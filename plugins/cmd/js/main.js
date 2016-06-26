(function() {
    cmd = {
		"run": function(command, callback) {
			data = {
				"cmd": command
			}
			url = "python://cmd/run";
			corefunctions.sendXHR(url, data, callback);
		}
	};
	return cmd;
})();
