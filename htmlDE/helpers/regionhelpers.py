from math import floor, ceil
import sys
import cairo


#Port of Gdk.cairo_region_create_from_surface as the native version Segfaults
#Sadly very slow, but I don't have any hope that the native function gets fixed any time soon.
def cairo_region_create_from_surface(surface, mask_accuracy):
    rect = cairo.RectangleInt()
    extents = _cairo_surface_extents(surface)
    if extents != False:
        if surface.get_content() == cairo.CONTENT_COLOR:
            return cairo.Region(extents)
        if type(surface) != cairo.ImageSurface or surface.get_format != cairo.FORMAT_A1:
            image = cairo.ImageSurface(cairo.FORMAT_A1, extents.width, extents.height)

            cr = cairo.Context(image)
            cr.set_source_surface(surface, -extents.x, -extents.y)
            cr.paint()
        else:
            image = surface

        image.flush()
        data = image.get_data()
        stride = image.get_stride()

        region = cairo.Region()
        for y in range(0, extents.height, mask_accuracy):
            for x in range(0, extents.width, mask_accuracy):
                x0 = x;
                while x < extents.width: 
                    if sys.byteorder == 'little':
                        if ((data[y*stride+x//8] >> (x%8)) & 1) == 0:
                            break
                    if sys.byteorder == 'big':
                        if ((data[y*stride+x//8] >> (7-(x%8))) & 1) == 0:
                            break
                    x += mask_accuracy

                if x > x0:
                    rect.x = x0
                    rect.width = x - x0
                    rect.y = y
                    rect.height = mask_accuracy
                    region.union(rect)

    region.translate(extents.x, extents.y)
    return region


def _cairo_surface_extents(surface):
    if surface == None:
        return False
    cr = cairo.Context(surface)
    x1, y1, x2, y2 = cr.clip_extents()
    x1 = floor(x1)
    y1 = floor(y1)
    x2 = ceil(x2)
    y2 = ceil(y2)
    x2 -= x1
    y2 -= y1

    extents = cairo.RectangleInt()
    extents.x = x1
    extents.y = y1
    extents.width = x2
    extents.height = y2

    return extents
