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
            alert(picture);
        })
        .catch(err => {
            console.error(err);
        })
}