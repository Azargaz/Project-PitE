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