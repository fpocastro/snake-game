//37: left
//38: up
//39: right
//40: down

var gameConfig = {
    width: 15,
    height: 15,
    fps: 100,
    snake: [
        { x: 8, y: 8 },
        { x: 9, y: 8 },
        { x: 10, y: 8 },
        { x: 11, y: 8 },
        { x: 12, y: 8 },
    ],
    direction: 37,
    allowedInputs: [37, 38, 39, 40]
};

var canvas, context, scoreBoard, direction, prevDirection, snake, game, food, score, inputQueue;
reset();
function reset() {
    canvas = document.getElementById('stage');
    context = canvas.getContext("2d");
    scoreBoard = document.getElementById('score');
    //context.clearRect(0, 0, canvas.width, canvas.height);
    direction = gameConfig.direction;
    snake = gameConfig.snake;
    score = 0;
    prevDirection = gameConfig.direction;
    inputQueue = [];

    do {
        food = generateFood(0, gameConfig.height - 1);
    } while (isOnSnake(food.x, food.y))

    game = window.setInterval(function () {
        direction = inputQueue.shift() || direction;
        switch (direction) {
            case 37:
                if (prevDirection == 39) {
                    snake.unshift({ x: snake[0].x + 1, y: snake[0].y });
                    direction = 39;
                } else {
                    snake.unshift({ x: snake[0].x - 1, y: snake[0].y });
                }
                break;
            case 38:
                if (prevDirection == 40) {
                    snake.unshift({ x: snake[0].x, y: snake[0].y + 1 });
                    direction = 40;
                } else {
                    snake.unshift({ x: snake[0].x, y: snake[0].y - 1 });
                }
                break;
            case 39:
                if (prevDirection == 37) {
                    snake.unshift({ x: snake[0].x - 1, y: snake[0].y });
                    direction = 37;
                } else {
                    snake.unshift({ x: snake[0].x + 1, y: snake[0].y });
                }
                break;
            case 40:
                if (prevDirection == 38) {
                    snake.unshift({ x: snake[0].x, y: snake[0].y - 1 });
                    direction = 38;
                } else {
                    snake.unshift({ x: snake[0].x, y: snake[0].y + 1 });
                }
                break;
            default:
                break;
        }


        prevDirection = direction;

        keyLock = false;

        if (snake[0].x < 0 || snake[0].x >= gameConfig.width || snake[0].y < 0 || snake[0].y >= gameConfig.height) {
            clearInterval(game);
            return;
        }

        for (var i = 1; i < snake.length; i++) {
            if (snake[0].x == snake[i].x && snake[0].y == snake[i].y) {
                clearInterval(game);
                return;
            }
        }

        if (snake[0].x == food.x && snake[0].y == food.y) {
            do {
                food = generateFood(0, gameConfig.height - 1);
            } while (isOnSnake(food.x, food.y))
            score++;
            scoreBoard.textContent = score;
        } else {
            snake.pop();
        }

        for (var i = 0; i < gameConfig.height; i++) {
            for (var j = 0; j < gameConfig.width; j++) {
                drawCell(i, j, 'rgb(255, 255, 255)');
            }
        }
        for (var i = 0; i < snake.length; i++) {
            drawCell(snake[i].x, snake[i].y, 'rgb(0, 0, 0)');
        }
        drawCell(food.x, food.y, 'rgb(255, 0, 0)');

    }, gameConfig.fps);
}

function drawCell(x, y, color) {
    context.fillStyle = color;
    context.beginPath();
    context.fillRect((x * gameConfig.width), (y * gameConfig.height), gameConfig.width, gameConfig.height);
};

function generateFood(min, max) {
    return {
        x: Math.floor(Math.random() * (max - min + 1)) + min,
        y: Math.floor(Math.random() * (max - min + 1)) + min
    };
}

function isOnSnake(x, y) {
    for (var i = 0; i < snake.length; i++) {
        if (snake[i].x == x && snake[i].y == y) {
            return true;
        }
    }
    return false;
}

document.onkeydown = function (event) {
    if (event.which == 32) {
        // clearInterval(game);
        // reset();
        location.reload();
    }
    if (gameConfig.allowedInputs.includes(event.which)) {
        if (inputQueue[inputQueue.length - 1] != event.which) {
            inputQueue.push(event.which);
        }
    }
};