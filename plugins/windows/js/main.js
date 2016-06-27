(function() {
	windows = {
		"events": {
			"newWindowCreated": "newWindowCreated"
		},
		"Window": function(url, x, y, width, height, transparent, type) {
			this.id = 0;
			data = {
				"url": url,
				"x": x,
				"y": y,
				"width": width,
				"height": height,
				"own": window.location
			};
			if(transparent !== undefined) {
				data.transparent = transparent;
			}
			url = "python://windows/create"+type;
			corefunctions.sendXHR(url, data, function(data) {
				this.id = data.result.id;
			}.bind(this));

		},
		"BackgroundWindow": function(url, x, y, width, height, transparent) {
			windows.Window.call(this, url, x, y, width, height, transparent, "BackgroundWindow");
		},
		"PanelWindow": function(url, x, y, width, height, transparent) {
			windows.Window.call(this, url, x, y, width, height, transparent, "PanelWindow");
		}
	}

	windows.Window.prototype.delete = function() {
		data = {
			"id": this.id
		};
		url = "python://windows/deleteWindow";
		corefunctions.sendXHR(url, data);
	}
	windows.Window.prototype.move = function(x, y) {
		data = {
			"id": this.id,
			"x": x,
			"y": y
		};
		url = "python://windows/moveWindow";
		corefunctions.sendXHR(url, data);
	}
	windows.Window.prototype.resize = function(width, height) {
		data = {
			"id": this.id,
			"width": width,
			"height": height
		};
		url = "python://windows/resizeWindow";
		corefunctions.sendXHR(url, data);
	}
	windows.Window.prototype.getPosition = function() {
		data = {
			"id": this.id
		};
		url = "python://windows/getWindowPosition";
		return corefunctions.sendSXHR(url, data);
	}
	windows.Window.prototype.getSize = function() {
		data = {
			"id": this.id
		};
		url = "python://windows/getWindowSize";
		return corefunctions.sendSXHR(url, data);
	}
	windows.BackgroundWindow.prototype = Object.create(windows.Window.prototype);
	windows.BackgroundWindow.prototype.constructor = windows.BackgroundWindow;
	windows.PanelWindow.prototype = Object.create(windows.Window.prototype);
	windows.PanelWindow.prototype.constructor = windows.PanelWindow;

	return windows
})();
