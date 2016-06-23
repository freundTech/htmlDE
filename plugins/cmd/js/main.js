(function() {
    cmd = {
		"run": function(command, callback) {
			/**$.ajax({
				url: "python://cmd/run",
				data: {
					"cmd": command
				},
				dataType: "json",
				success: callback
			});**/
			request = new XMLHttpRequest();
			request.onreadystatechange = function() {
				if(request.readyState == 4) {
					result = JSON.parse(request.responseText);
					callback(result);
				}
			}
			request.open("GET", "python://cmd/run?cmd="+command, true);
			request.send();
		}
	};
	return cmd;
})();
