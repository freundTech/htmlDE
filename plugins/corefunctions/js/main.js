(function() {
	var corefunctions = {
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
		},
		"EventHandler": function(events) {
			this.handlers = [];
			for(var id in events) {
				this.handlers[events[id]] = [];
			}
		}
	}
	corefunctions.EventHandler.prototype.listen = function(name, callback) {
		if(name in this.handlers) {
			this.handlers[name].push(callback);
		}
	}
	corefunctions.EventHandler.prototype.dispatch = function(name, data) {
		if(name in this.handlers) {
			for(var i in this.handlers[name]) {
				this.handlers[name][i](data);
			}
		}
	}

	return corefunctions

})();
