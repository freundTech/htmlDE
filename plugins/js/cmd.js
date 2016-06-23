(function() {
    cmd = {
		"run": function(command, callback) {
			$.ajax({
				url: "python://cmd/run",
				data: {
					"cmd": command
				},
				dataType: "json",
				success: callback
			});
		}
	};
	return cmd;
})();
