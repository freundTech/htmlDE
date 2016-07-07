(function() {
	desktops = {
		"getCurrentDesktop": function() {
			url = "python://desktops/getCurrentDesktop";
			return corefunctions.sendSXHR(url, {});
		},
		"getDesktopNames": function() {
			url = "python://desktops/getDesktopNames";
			return corefunctions.sendSXHR(url, {});
		},
		"getNumberOfDesktop": function() {
			url = "python://desktops/getNumberOfDesktops";
			return corefunctions.sendSXHR(url, {});
		},
		"setCurrentDesktop": function(desktop) {
			data = {
				"desktop": desktop
			}
			url = "python://desktops/setCurrentDesktop";
			corefunctions.sendXHR(url, data);
		},
		"events": new plugins.corefunctions.EventHandler(["desktopChanged"])
	}

	return desktops
})();
