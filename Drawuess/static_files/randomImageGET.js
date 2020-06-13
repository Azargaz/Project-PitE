var picture = ''
    answered = false
    interval = 2000;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const showImage = (image) => {
    let pixels = [];
    for(row of image) for (e of row) pixels.push(e);

    let width = 28;
    let height = 28;

    // Create canvas
    let canvas = document.getElementById('picture_extended');
    let context = canvas.getContext('2d');
    let imgData = context.createImageData(width, height);

    for(let i = 0; i < pixels.length * 4; i+=4) {
        pixel = Number(pixels[i/4]) * 255;
        imgData.data[i] = pixel;
        imgData.data[i + 1] = pixel;
        imgData.data[i + 2] = pixel;
        imgData.data[i + 3] = 255;
    }

    context.putImageData(imgData, 0, 0);
}

const getImage = () => {
    const csrftoken = getCookie('csrftoken');

    fetch('http://127.0.0.1:8000/picture_extended/', {
        method: 'GET',
        cors: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(json => {
            picture = json.picture;
            console.log(`similar to: ${json.similar_to}\noriginal category: ${json.category}`);
            showImage(JSON.parse(picture));
        })
        .catch(err => {
            console.error(err);
        })
}