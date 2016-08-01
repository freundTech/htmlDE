(function() {
	var desktops = {
		"getCurrentDesktop": function() {
			var url = "python://desktops/getCurrentDesktop";
			return plugins.corefunctions.sendSXHR(url, {});
		},
		"getDesktopNames": function() {
			var url = "python://desktops/getDesktopNames";
			return plugins.corefunctions.sendSXHR(url, {});
		},
		"getNumberOfDesktop": function() {
			var url = "python://desktops/getNumberOfDesktops";
			return plugins.corefunctions.sendSXHR(url, {});
		},
		"setCurrentDesktop": function(desktop) {
			var data = {
				"desktop": desktop
			};
			var url = "python://desktops/setCurrentDesktop";
			plugins.corefunctions.sendXHR(url, data);
		},
		"events": new plugins.corefunctions.EventHandler(["desktopChanged"])
	};

	return desktops;
})();
