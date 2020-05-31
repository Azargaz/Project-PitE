var canvas, ctx;
var interval = 2000;
var curX = 0,
    curY = 0,
    prevX = 0,
    prevY = 0
    w = 0,
    h = 0;

var drawFlag = false
    drawDotFlag = false
    strokeColor = 'black'
    bgColor = 'white'
    lineWidth = 10
    answer = ''
    answered = false;

const init = () => {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    w = canvas.width;
    h = canvas.height;
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, w, h);
    canvas.addEventListener("mousemove", draw, false);
    canvas.addEventListener("mousedown", (event) => {
        drawFlag = true;
        drawDot(event);
    }, false);
    canvas.addEventListener("mouseup", () => {
        drawFlag = false;
    }, false);
}

const clearCanvas = () => {
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, w, h);
}

const drawDot = (event) => {
    prevX = curX;
    prevY = curY;
    curX = event.clientX - canvas.offsetLeft - lineWidth;
    curY = event.clientY - canvas.offsetTop - lineWidth;

    flag = true;
    drawDotFlag = true;
    if (drawDotFlag) {
        ctx.beginPath();    
        ctx.strokeStyle = strokeColor;
        ctx.fillStyle = strokeColor;
        ctx.lineWidth = lineWidth;
        ctx.arc(curX, curY, lineWidth/8, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
        ctx.closePath();
        drawDotFlag = false;
    }
}

const draw = (event) => {
    prevX = curX;
    prevY = curY;
    curX = event.clientX - canvas.offsetLeft - lineWidth;
    curY = event.clientY - canvas.offsetTop - lineWidth;

    if(!drawFlag) return;
    ctx.beginPath();    
	ctx.lineCap = 'round';
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = lineWidth;
    
	ctx.moveTo(prevX, prevY);
	ctx.lineTo(curX, curY);
    ctx.stroke();

    ctx.closePath();
}

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
            if(answer.localeCompare(to_draw_item))
            {
                updateBadAnswer();
                setTimeout(guessImage, interval);
            }
            else
            {
                updateGoodAnswer();
                answered = true;
            }
        })
        .catch(err => {
            console.error(err);
        })
}

const startGuessing = () => {
    answered = false;
    setTimeout(guessImage, interval);
}

const updateGoodAnswer = () => {
    answerElement = document.getElementById('answer')
    if(answer !== '') {
        answerElement.innerHTML = "I got it! You're drawing: " + answer;
    }
}

const updateBadAnswer = () => {
    answerElement = document.getElementById('answer')
    if(answer !== '') {
        answerElement.innerHTML = "So close! I thought it was: " + answer;
    }
}