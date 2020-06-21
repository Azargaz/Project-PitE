const updateAnswer = () => {
	answerElement = document.getElementById('answer');
	if (answer !== '') {
		answerElement.innerHTML =
			'Did you ment to draw ' +
			answer +
			'?' +
			'<button onclick = answerButtonYes() class="btn btn-secondary btn-sm"> yes </button>' +
			'&nbsp;<button onclick = answerButtonNo() class="btn btn-secondary btn-sm"> no </button>';
	}
};

const checkImage = () => {
	guessImage();
};

const answerButtonYes = () => {
	answerElement = document.getElementById('answer');
	console.log(`a: ${answer}\np: ${similar_to}`);
	if (answer === similar_to) {
		answerElement.innerHTML = 'That is correct answer!';
	} else {
		answerElement.innerHTML = "That is not what you should have drawn.";
	}
};

const answerButtonNo = () => {
	answerElement = document.getElementById('answer');
	answerElement.innerHTML =
		'That\'s a pity, try to draw again <button onclick = clearCanvas() class="btn btn-secondary btn-sm"> Clear </button>';
};
