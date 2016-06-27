(function() {
	corefunctions = {
		"encodeQuery": function(obj) {
			var str = [];
			for(var p in obj) {
				if(obj.hasOwnProperty(p)) {
					str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
				}
			}
			return str.join("&");
		},
		"sendXHR": function(url, data, callback) {
			request = new XMLHttpRequest();
			if(callback !== undefined) {
				request.onreadystatechange = function() {
					if(request.readyState == 4) {
						callback(JSON.parse(request.responseText));
					}
				};
			}
			request.open("GET", url+"?"+corefunctions.encodeQuery(data), true);
			request.send();
		},
		"sendSXHR": function(url, data) {
			request = new XMLHttpRequest();
			request.open("GET", url+"?"+corefunctions.encodeQuery(data), false);
			request.send();

			result = JSON.parse(request.responseText);
			if(result.status === 0) {
				return result.result;
			}
		}

	}

	return corefunctions

})();
