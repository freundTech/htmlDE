(function() {
	var windows = {
		"events": {
			"newWindowCreated": "newWindowCreated"
		},
		"Window": function(url, x, y, width, height, transparent, type) {
			this.id = 0;
			var data = {
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
			var url = "python://windows/create"+type;
			plugins.corefunctions.sendXHR(url, data, function(data) {
				this.id = data.result.id;
			}.bind(this));

		},
		"BackgroundWindow": function(url, x, y, width, height, transparent) {
			windows.Window.call(this, url, x, y, width, height, transparent, "BackgroundWindow");
		},
		"PanelWindow": function(url, x, y, width, height, transparent) {
			windows.Window.call(this, url, x, y, width, height, transparent, "PanelWindow");
		}
	};

	windows.Window.prototype.delete = function() {
		var data = {
			"id": this.id
		};
		var url = "python://windows/deleteWindow";
		plugins.corefunctions.sendXHR(url, data);
	};
	windows.Window.prototype.move = function(x, y) {
		var data = {
			"id": this.id,
			"x": x,
			"y": y
		};
		var url = "python://windows/moveWindow";
		plugins.corefunctions.sendXHR(url, data);
	};
	windows.Window.prototype.resize = function(width, height) {
		var data = {
			"id": this.id,
			"width": width,
			"height": height
		};
		var url = "python://windows/resizeWindow";
		plugins.corefunctions.sendXHR(url, data);
	};
	windows.Window.prototype.getPosition = function() {
		var data = {
			"id": this.id
		};
		var url = "python://windows/getWindowPosition";
		return plugins.corefunctions.sendSXHR(url, data);
	};
	windows.Window.prototype.getSize = function() {
		var data = {
			"id": this.id
		};
		var url = "python://windows/getWindowSize";
		return plugins.corefunctions.sendSXHR(url, data);
	};
	windows.BackgroundWindow.prototype = Object.create(windows.Window.prototype);
	windows.BackgroundWindow.prototype.constructor = windows.BackgroundWindow;
	windows.PanelWindow.prototype = Object.create(windows.Window.prototype);
	windows.PanelWindow.prototype.constructor = windows.PanelWindow;

	return windows;
})();
