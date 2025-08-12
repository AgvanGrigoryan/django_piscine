function updateUsername() {
	fetch('/api/username')
		.then(response => response.json())
		.then(data => {
			document.getElementById('username').textContent = data.username
		});

	}
setInterval(updateUsername, 1000)

updateUsername();