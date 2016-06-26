def ensureArguments(*args):
    for i, arg in enumerate(args):
        if arg == None:
            raise ArgumentsError("Argument {} is None".format(i))
    return True

def normalizeArguments(*args):
    for i, arg in enumerate(args):
        try:
            if len(arg) == 1:
                args[i] = args[i][0]
        except:
            pass
    return args


def sendEvent(pluginname, eventname, data):
    pass
