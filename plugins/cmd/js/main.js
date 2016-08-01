(function() {
    var cmd = {
		"run": function(command, callback) {
			var data = {
				"cmd": command
			};
			var url = "python://cmd/run";
			plugins.corefunctions.sendXHR(url, data, callback);
		}
	};
	return cmd;
})();
