var origBoard;
var string_hash = "________________";
var huPlayer = 'X';
var aiPlayer = 'O';

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
    string_hash = "________________"
    checkWin("X").then((gameWon) => {
        if (gameWon.player && !checkTie()) { gameOver(gameWon) }
        else if (aiPlayer === "X") { turn(gameWon.solution, aiPlayer) }
    })
}

function switchSides() {
    huPlayer = (huPlayer === "X") ? "O" : "X";
    aiPlayer = (aiPlayer === "O") ? "X" : "O";
    startGame();
}

function checkWin(player) {
    return fetchJson(player).then(function(myJson) {
        console.log(myJson)
        var mapping = myJson.primitiveState.map((val)=>{
            return val[0] * 4 + val[1];
        });
        let gameWon = {
            solution : (myJson.solution) ? myJson.solution[0] * 4 + myJson.solution[1] : null,
            player : null,
            index : mapping
        };
        if (myJson.primitive === "Lose") {
            gameWon.player = huPlayer === player ? aiPlayer : huPlayer;        
        }
        if (myJson.primitive === "Win") {
            gameWon.player = player;
        }
        return gameWon;
    })
}

function turnClick(square) {
    if (typeof origBoard[square.target.id] == 'number') {
        turn(square.target.id, huPlayer).then(function(gameWon) {
            if (!gameWon.player) { turn(gameWon.solution, aiPlayer) }    
        });
    }
}

function turn(squareId, player) {
    origBoard[squareId] = player;
    string_hash = ""
    for (var i = 0; i < origBoard.length; i++) {
        if (origBoard[i] == aiPlayer) {
            string_hash += aiPlayer;   
        }
        else if (origBoard[i] == huPlayer) {
            string_hash += huPlayer;
        }
        else {
            string_hash += "_";
        }
    }
    document.getElementById(squareId).innerText = player;
    return checkWin((player === huPlayer) ? aiPlayer : huPlayer).then(function(gameWon) {
        if (gameWon.player && !checkTie()) { gameOver(gameWon); }
        return gameWon;   
    }); 
}

function gameOver(gameWon) {
    for (let index of gameWon.index) {
        document.getElementById(index).style.backgroundColor = 
            gameWon.player == huPlayer ? "blue" : "red";
    }
    for (var i = 0; i < cells.length; i++) {
        cells[i].removeEventListener('click', turnClick, false);
    }
    declareWinner(gameWon.player == huPlayer ? "You Win!" : "You lose");
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

function declareWinner(who) {
    document.querySelector(".endgame").style.display = "block";
    document.querySelector(".endgame .text").innerText = who;
}

function emptySquares() {
    return origBoard.filter(s => (typeof s) == 'number')
}

function fetchJson(player) {
    return fetch('/solver/' + player + '/' + string_hash).then(function(response) {
        return response.json();
    })
}
