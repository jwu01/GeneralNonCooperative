var animationClasses = [
    'confetti__item--animation1',
    'confetti__item--animation2',
    'confetti__item--animation3',
    'confetti__item--animation4',
    'confetti__item--animation5',
    'confetti__item--animation6',
    'confetti__item--animation7',
    'confetti__item--animation8',
    'confetti__item--animation9',
];

var colourClasses = [
    'confetti__item--colour1',
    'confetti__item--colour2',
    'confetti__item--colour3',
    'confetti__item--colour4',
    'confetti__item--colour5',
];

function StartConfetti()
{
  for(let i = 0; i < 400; i++) {
    var newNode = document.createElement('div');
    var randomClass = animationClasses[Math.floor(Math.random() * animationClasses.length)];
    var randomColour = colourClasses[Math.floor(Math.random() * colourClasses.length)];
    var animationDelay = parseFloat(Math.min(0 + (Math.random() * (5 - 0)), 5).toFixed(2)) + "s";
    var left = Math.floor(Math.random() * (100 - 0 + 1)) + 0 + "vw";
    
    newNode.className = 'confetti__item ' + randomClass + ' ' + randomColour;
    
    newNode.setAttribute("style", "animation-delay: " + animationDelay + "; left: " + left + ";");
      
    document.getElementById('confetti').appendChild(newNode);
  }
}