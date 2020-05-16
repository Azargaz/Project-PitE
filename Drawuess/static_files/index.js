var canvas, ctx;

var curX = 0,
    curY = 0,
    prevX = 0,
    prevY = 0
    w = 0,
    h = 0;

var drawFlag = false
    drawDotFlag = false
    strokeColor = "black"
    lineWidth = 20
    answer = '';

const init = () => {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    w = canvas.width;
    h = canvas.height;
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
    ctx.clearRect(0, 0, w, h);
}

const drawDot = (event) => {
    prevX = curX;
    prevY = curY;
    curX = event.clientX - canvas.offsetLeft;
    curY = event.clientY - canvas.offsetTop;

    flag = true;
    drawDotFlag = true;
    if (drawDotFlag) {
        ctx.beginPath();
        ctx.fillStyle = strokeColor;
        ctx.fillRect(curX, curY, 2, 2);
        ctx.closePath();
        drawDotFlag = false;
    }
}

const draw = (event) => {
    prevX = curX;
    prevY = curY;
    curX = event.clientX - canvas.offsetLeft;
    curY = event.clientY - canvas.offsetTop;

    if(!drawFlag) return;
    ctx.beginPath();

    var dl = 20 + Math.sqrt((curX-prevX)*(curX-prevX));
    var szer = 20 + Math.sqrt((curY-prevY)*(curY-prevY));
    ctx.fillRect(curX, curY,dl,szer);
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = lineWidth;
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
var csrftoken = getCookie('csrftoken');
const saveImage = () => {
    const dataURL = canvas.toDataURL();

    fetch('http://127.0.0.1:8000/picture/', {
        method: 'POST',
        cors: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataURL)
    })
        .then(response => response.json())
        .then(json => {
            console.log(json);
            answer = json.result;
            if(answer.localeCompare(to_draw_item))
            {
                updateGoodAnswer();
            }
            else
            {
                updateBadAnswer();
            }

        })
}

const updateGoodAnswer = () => {
    answerElement = document.getElementById('answer')
    if(answer !== '') {
        answerElement.innerHTML = "YAY! You're drawing: " + answer;
    }
}

const updateBadAnswer = () => {
    answerElement = document.getElementById('answer')
    if(answer !== '') {
        answerElement.innerHTML = "Damn! I thought it was: " + answer;
    }
}