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
		}
	}

	return corefunctions

})();
