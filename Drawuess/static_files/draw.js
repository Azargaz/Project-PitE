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
    lineWidth = 5
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
    curX = event.clientX - canvas.offsetLeft;
    curY = event.clientY - canvas.offsetTop;

    flag = true;
    drawDotFlag = true;
    if (drawDotFlag) {
        ctx.beginPath();    
        ctx.arc(curX - lineWidth, curY - lineWidth, lineWidth, 0, 2 * Math.PI);
        ctx.strokeStyle = strokeColor;
        ctx.fillStyle = strokeColor;
        ctx.lineWidth = lineWidth;
        ctx.fill();
        ctx.stroke();
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
    ctx.arc(curX - lineWidth, curY - lineWidth, lineWidth, 0, 2 * Math.PI);
    ctx.strokeStyle = strokeColor;
    ctx.fillStyle = strokeColor;
    ctx.lineWidth = lineWidth;
    ctx.fill();
    ctx.stroke();

    ctx.closePath();
}