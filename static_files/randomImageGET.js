var picture = '';
answered = false;
interval = 2000;
similar_to = '';

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + '=') {
				cookieValue = decodeURIComponent(
					cookie.substring(name.length + 1)
				);
				break;
			}
		}
	}
	return cookieValue;
}

const showImage = (image, name) => {
	let pixels = [];
	for (row of image) for (e of row) pixels.push(e);

	let width = 28;
	let height = 28;

	// Create canvas
	let canvas = document.createElement('canvas');
	canvas.width = width;
	canvas.height = height;
	let context = canvas.getContext('2d');
	let imgData = context.createImageData(width, height);

	for (let i = 0; i < pixels.length * 4; i += 4) {
		pixel = (1.0 - Number(pixels[i / 4])) * 255;
		imgData.data[i] = pixel;
		imgData.data[i + 1] = pixel;
		imgData.data[i + 2] = pixel;
		imgData.data[i + 3] = 255;
	}

	context.putImageData(imgData, 0, 0);
	document.getElementById(name).src = canvas.toDataURL();
};

const getImage = () => {
	const csrftoken = getCookie('csrftoken');

	fetch('http://127.0.0.1:8000/get_random_similars/4/', {
		method: 'GET',
		cors: 'same-origin',
		headers: {
			'X-CSRFToken': csrftoken,
			'Content-Type': 'application/json',
		},
	})
		.then((response) => response.json())
		.then((json) => {
			pictures = JSON.parse(json.pictures);
			similar_to = json.similar_to;
			console.log(
				`similar to: ${json.similar_to}`
			);
			showImage(pictures[0], 'img1');
			showImage(pictures[1], 'img2');
			showImage(pictures[2], 'img3');
			showImage(pictures[3], 'img4');
		})
		.catch((err) => {
			console.error(err);
		});
};
