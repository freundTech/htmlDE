(function() {
	var taskbar = {
		"events": new plugins.corefunctions.EventHandler(["windowAdded", "windowRemoved"]),
		"Window": function(id) {
			this.id = id;
		},
		"getWindows": function(stacked, desktop) {
			var data = {};
			if(stacked !== undefined) {
				data.stacked = stacked;
			}
			if(desktop !== undefined) {
				data.desktop = desktop;
			}
			var url = "python://taskbar/getWindows";
			var list = plugins.corefunctions.sendSXHR(url, data);
			var windows = [];
			for(i in list) {
				windows.push(new taskbar.Window(list[i]));
			}
			return windows;
		},
		"getActiveWindow": function() {
			var url = "python://taskbar/getActiveWindow";
			var id = plugins.corefunctions.sendSXHR(url);
			return new taskbar.Window(id);
		},
		"getPreviouslyActiveWindow": function() {
			var url = "python://taskbar/getPreviouslyActiveWindow";
			var id = plugins.corefunctions.sendSXHR(url);
			return new taskbar.Window(id);
		}
	}
	taskbar.Window.prototype.getName = function() {
		var data = {
			"xid": this.id
		};
		var url = "python://taskbar/getWindowName";
		return plugins.corefunctions.sendSXHR(url, data);
	}
	taskbar.Window.prototype.getIconUrl = function() {
		return "python://taskbar/getWindowIcon?xid="+this.id;
	}
	taskbar.Window.prototype.getGroup = function() {
		var data = {
			"xid": this.id
		};
		var url = "python://taskbar/getWindowGroup";
		return plugins.corefunctions.sendSXHR(url, data);
	}
	taskbar.Window.prototype.close = function() {
		var data = {
			"xid": this.id
		};
		var url = "python://taskbar/closeWindow";
		return plugins.corefunctions.sendXHR(url, data);
	}
	taskbar.Window.prototype.activate = function() {
		var data = {
			"xid": this.id
		};
		var url = "python://taskbar/activateWindow";
		return plugins.corefunctions.sendXHR(url, data);
	}
	taskbar.Window.prototype.minimize = function() {
		var data = {
			"xid": this.id
		};
		var url = "python://taskbar/minimizeWindow";
		return plugins.corefunctions.sendXHR(url, data);
	}
	taskbar.Window.prototype.isMinimized = function() {
		var data = {
			"xid": this.id
		};
		var url = "python://taskbar/isWindowMinimized";
		return plugins.corefunctions.sendSXHR(url, data);
	}
	taskbar.Window.prototype.needsAttention = function() {
		var data = {
			"xid": this.id
		};
		var url = "python://taskbar/getWindowNeedsAttention";
		return plugins.corefunctions.sendSXHR(url, data);
	}

	return taskbar;
})();
