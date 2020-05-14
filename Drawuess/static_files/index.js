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
    lineWidth = 20;

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
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(curX, curY);
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
const saveImage = async () => {
    const dataURL = canvas.toDataURL();
    console.log(dataURL);
    const response = await fetch('http://127.0.0.1:8000/picture/', {
        method: 'POST',
        cors: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataURL)
    });
    console.log(response);
}