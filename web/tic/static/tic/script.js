var origBoard;
var string_hash = "";
var huPlayer = 'X';
var aiPlayer = 'O';
const winCombos = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 10, 11],
    [12, 13, 14, 15],
    [0, 4, 8, 12],
    [1, 5, 9, 13],
    [2, 6, 10, 14],
    [3, 7, 11, 15],
    [0, 5, 10, 15],
    [3, 6, 9, 12]
]

const cells = document.querySelectorAll('.cell');
startGame();

function startGame() {
    document.querySelector(".endgame").style.display = "none";
    origBoard = Array.from(Array(16).keys());
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
            string_hash += "O";   
        }
        else if (origBoard[i] == huPlayer) {
            string_hash += "X";
        }
        else {
            string_hash += "_";
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
        return myJson.solution[0] * 4 + myJson.solution[1];
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
