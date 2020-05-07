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
    lineWidth = 2;

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

const saveImage = async () => {
    const dataURL = canvas.toDataURL();
    const response = await fetch('http://localhost:8888/', {
        method: 'POST',
        cors: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataURL)
    });
    console.log(response);
}