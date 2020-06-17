var answer = ''
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

const guessImage = () => {
    const dataURL = canvas.toDataURL();
    const csrftoken = getCookie('csrftoken');

    fetch('http://127.0.0.1:8000/picture/', {
        method: 'POST',
        cors: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataURL),

    })
        .then(response => response.json())
        .then(json => {
            answer = json.result;
            updateAnswer();
        })
        .catch(err => {
            console.error(err);
        })
}