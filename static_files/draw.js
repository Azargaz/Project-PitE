var canvas, ctx;

var curX = 0,
	curY = 0,
	prevX = 0,
	prevY = 0;
(w = 0), (h = 0);

var drawFlag = false;
drawDotFlag = false;
strokeColor = 'black';
bgColor = 'white';
lineWidth = 10;

function offset(elem) {
	if (!elem) elem = this;

	var x = elem.offsetLeft;
	var y = elem.offsetTop;

	while ((elem = elem.offsetParent)) {
		x += elem.offsetLeft;
		y += elem.offsetTop;
	}

	return { left: x, top: y };
}

const init = () => {
	canvas = document.getElementById('canvas');
	ctx = canvas.getContext('2d');
	w = canvas.width;
	h = canvas.height;
	ctx.fillStyle = bgColor;
	ctx.fillRect(0, 0, w, h);
	canvas.addEventListener('mousemove', draw, false);
	canvas.addEventListener(
		'mousedown',
		(event) => {
			drawFlag = true;
			drawDot(event);
		},
		false
	);
	canvas.addEventListener(
		'mouseup',
		() => {
			drawFlag = false;
		},
		false
	);
};

const clearCanvas = () => {
	ctx.fillStyle = bgColor;
	ctx.fillRect(0, 0, w, h);
};

const drawDot = (event) => {
	prevX = curX;
	prevY = curY;
	off = offset(canvas);
	curX = event.clientX - off.left;
	curY = event.clientY - off.top;

	flag = true;
	drawDotFlag = true;
	if (drawDotFlag) {
		ctx.beginPath();
		ctx.arc(
			curX - lineWidth / 8,
			curY - lineWidth / 8,
			lineWidth / 8,
			0,
			2 * Math.PI
		);
		ctx.strokeStyle = strokeColor;
		ctx.fillStyle = strokeColor;
		ctx.lineWidth = lineWidth;
		ctx.fill();
		ctx.stroke();
		ctx.closePath();
		drawDotFlag = false;
	}
};

const draw = (event) => {
	prevX = curX;
	prevY = curY;
	off = offset(canvas);
	curX = event.clientX - off.left;
	curY = event.clientY - off.top;

	if (!drawFlag) return;
	ctx.beginPath();
	ctx.moveTo(prevX, prevY);
	ctx.lineTo(curX, curY);
	ctx.lineCap = 'round';
	ctx.strokeStyle = strokeColor;
	ctx.lineWidth = lineWidth;
	ctx.stroke();
	ctx.closePath();
};
