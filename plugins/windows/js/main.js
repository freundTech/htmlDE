(function() {
	windows = {
		"events": {
			"newWindowCreated": "newWindowCreated"
		},
		"createBackgroundWindow": function(name, url, x, y, width, height, transparent) {
			data = {
				"name": name,
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
			url = "python://windows/createBackgroundWindow";
			corefunctions.sendXHR(url, data);
		},
		"createPanelWindow": function(name, url, x, y, width, height, transparent) {
			data = {
				"name": name,
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
			url = "python://windows/createPanelWindow";
			corefunctions.sendXHR(url, data);
		},
		"deleteWindow": function(name) {
			data = {
				"name": name
			};
			url = "python://windows/deleteWindow";
			corefunctions.sendXHR(url, data);
		},
		"moveWindow": function(name, x, y) {
			data = {
				"name": name,
				"x": x,
				"y": y
			};
			url = "python://windows/moveWindow";
			corefunctions.sendXHR(url, data);
		}
	}

	return windows
})();
