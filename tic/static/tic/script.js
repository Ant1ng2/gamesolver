var origBoard;
var string_hash = "";
var huPlayer = 'X';
var aiPlayer = 'O';
const winCombos = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [6, 4, 2],
]

const cells = document.querySelectorAll('.cell');
startGame();

function startGame() {
    document.querySelector(".endgame").style.display = "none";
    origBoard = Array.from(Array(9).keys());
    for (var i = 0; i < cells.length; i++) {
        cells[i].innerText = '';
        cells[i].style.removeProperty('background-color');
        cells[i].addEventListener('click', turnClick, false);
    }
}

function switchSides() {
    startGame();
    huPlayer = (huPlayer === "X") ? "O" : "X";
    aiPlayer = (aiPlayer === "O") ? "X" : "O";
}

function turnClick(square) {
    if (typeof origBoard[square.target.id] == 'number') {
        turn(square.target.id, huPlayer);
        let gameWon = checkWin(origBoard, huPlayer);
        if (!gameWon && !checkTie()) {
            loadSolution().then(value => {turn(value, aiPlayer);})
   
        }
    }
}

function turn(squareId, player) {
    origBoard[squareId] = player;
    string_hash = ""
    for (var i = 0; i < origBoard.length; i++) {
        if (origBoard[i] == aiPlayer) {
            string_hash += "2";   
        }
        else if (origBoard[i] == huPlayer) {
            string_hash += "1";
        }
        else {
            string_hash += "0";
        }
    }
    document.getElementById(squareId).innerText = player;
    let gameWon = checkWin(origBoard, player); 
    let gameTie = checkTie()
    if (gameWon) {
        gameOver(gameWon);
    }
    else {
        checkTie();
    }
}

function checkWin(board, player) {
    let plays = board.reduce((a, e, i) =>
        (e === player) ? a.concat(i) : a, []);
    let gameWon = null;
    for (let [index, win] of winCombos.entries()) {
        if (win.every(elem => plays.indexOf(elem) > -1)) {
            gameWon = {index: index, player: player};
            break;
        }
    }
    return gameWon;
}

function gameOver(gameWon) {
    for (let index of winCombos[gameWon.index]) {
        document.getElementById(index).style.backgroundColor = 
            gameWon.player == huPlayer ? "blue" : "red";
    }
    for (var i = 0; i < cells.length; i++) {
        cells[i].removeEventListener('click', turnClick, false);
    }
    declareWinner(gameWon.player == huPlayer ? "You Win!" : "You lose");
}

function declareWinner(who) {
    document.querySelector(".endgame").style.display = "block";
    document.querySelector(".endgame .text").innerText = who;
}

function emptySquares() {
    return origBoard.filter(s => (typeof s) == 'number')
}

function loadSolution() {
    return fetch('/solver/' + aiPlayer + '/' + string_hash).then(function(response) {
        return response.json();
    })
    .then(function(myJson) {
        console.log(myJson);
        return myJson.solution[0] * 3 + myJson.solution[1];
    })
}

function checkTie() {
    if (emptySquares().length == 0) {
        for (var i = 0; i < cells.length; i++) {
            cells[i].style.backgroundColor = "green";
            cells[i].removeEventListener('click', turnClick, false);
        }
        declareWinner("Tie Game!");
        return true;
    }
    return false;
}
