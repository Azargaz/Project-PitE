
const updateAnswer = () => {
    answerElement = document.getElementById('answer')
    if(answer.result !== '') {
        answerElement.innerHTML= 'Did you ment to draw ' + answer.result + '?' + '<button onclick = answerButtonYes() class="btn btn-secondary btn-sm"> yes </button>'
        + '&nbsp;<button onclick = answerButtonNo() class="btn btn-secondary btn-sm"> no </button>'
    }
}


const checkImage = () => {
    guessImage();

}

const answerButtonYes = () => {
    answerElement = document.getElementById('answer')
    console.log(`a: ${answer.result}\np: ${similar_to}`);
    if(answer.result === similar_to) {
        answerElement.innerHTML= 'GREAT!!'
    }
    else{
        answerElement.innerHTML= 'That wasn\'t what you should have drawn.'
    }

}

const answerButtonNo = () => {
    answerElement = document.getElementById('answer')
    if(answer.similar_to !== '') {
        answerElement.innerHTML= 'That\'s a pity, try to draw again <button onclick = clearCanvas() class="btn btn-secondary btn-sm"> Clear </button>'

    }

}

// function check_if_true(guessed_image)
// {
//     answerElement = document.getElementById('answer');
//     if(guessed_image == answer)
//     {
//         updateGoodAnswer();
//     }
//     else{
//         updateBadAnswer();
//     }
// }

