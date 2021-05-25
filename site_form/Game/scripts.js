// Данные Зрителя
const accountHesh = 'test1';
let personalSnakeId = accountHesh;

// Данные Игроков: Hesh <=> Name
//const playersHesh = JSON.parse(``);

// Карта Игры
const gameReplay = JSON.parse(`{"players": ["test1", "das"],
"gameSettings": {"height": 10, "weight": 10},
"frames":
    [{"snakes": {"test1": [[8, 7], [2, 5]]},"apples": []},
    {"snakes": {"test1": [[8, 8], [3, 6]]}, "apples": [[0, 2], [9, 6], [0, 6]]},
    {"snakes": {"test1": [[7, 8], [4, 7]]}, "apples": [[0, 2], [9, 6], [0, 6]]},
    {"snakes": {"test1": [[7, 7], [5, 7]]}, "apples": [[0, 2], [9, 6], [0, 6]]},
    {"snakes": {"test1": [[8, 7], [6, 7]]}, "apples": [[0, 2], [9, 6], [0, 6]]},
    {"snakes": {"test1": [[8, 8], [7, 8]]}, "apples": [[0, 2], [9, 6], [0, 6]]},
    {"snakes": {}, "apples": [[0, 2], [9, 6], [0, 6]]}]}`.replaceAll("&#34;", '"'));

// HTML лементы
const canvas  = document.getElementById("game_screen");
const ctx = canvas.getContext('2d');

// Кнопка остановки - запуска
let gameStopped = true;
const btnStop  = document.getElementById("stop");
btnStop.addEventListener("click", stopButtonClick);


console.log(gameReplay);

let frameCount = 0;
let frameStep = 1;

const height = gameReplay.gameSettings.height;
const width = gameReplay.gameSettings.weight;
let step_x = Math.floor(canvas.width / width);
let step_y = Math.floor(canvas.height / height);
	step_x = Math.min(step_x, step_y);
	step_y = step_x;

// Прокрутка видео
let slider = document.getElementById("ReplayRange");
slider.setAttribute("max", gameReplay.frames.length - 1);
slider.oninput = function() {
    frameCount = parseInt(this.value);
	console.log("set value range", frameCount);
	drawFrame(frameCount);
}

// Кнопка reverse
const reverse = document.getElementById("reverse");
reverse.addEventListener("click", reverseButtonClick);

function reverseButtonClick() {
	if (frameStep === 1)
		reverse.value = "normal";
	else
	{
		reverse.value = "reverse";
	}
	frameStep *= -1;
}

// Скорость
let speedSelection = document.getElementById("speed_selection");

function stopButtonClick() {
	if (gameStopped) {
		btnStop.value = "Остановить";
	} else {
		btnStop.value = "Запуск";
	}
	gameStopped = !gameStopped;
}

function drawField() {
	/* Рисуем поле */
	ctx.fillStyle = "#ffffff";
	ctx.fillRect(0, 0, canvas.width, canvas.height);

	// ?
	ctx.strokeStyle = "#bee5ff";
	for (let j = step_x; j < canvas.width; j += step_x) {
		ctx.beginPath();
		ctx.moveTo(j, 0);
		ctx.lineTo(j, canvas.height);
		ctx.closePath();
		ctx.stroke();
	}
	for (let j = step_y; j < canvas.height; j += step_y) {
		ctx.beginPath();
		ctx.moveTo(0, j);
		ctx.lineTo(canvas.width, j);
		ctx.closePath();
		ctx.stroke();
	}
}

function drawFood(x, y) {
	/* Рисуем еду */
	let radius = Math.floor(Math.min(step_x, step_y) / 2);
	ctx.fillStyle = '#00ff00';
	ctx.beginPath();
	ctx.arc((x + 0.5) * step_x, (y + 0.5) * step_y, radius, 0, 2*Math.PI, false);
	ctx.closePath();
	ctx.fill();
}

function drawSnakeElement(x, y) {
	/* Рисуем элемент тела змейки */
	ctx.fillRect(x * step_x, y * step_y, step_x, step_y);
}

function drawSnakeHead(x, y) {
	/* Рисуем гогову змейки */
	ctx.fillRect(x * step_x, y * step_y, step_x, step_y);

	let tempColor = ctx.fillStyle;
	ctx.fillStyle = "#000000";

	ctx.beginPath();
	let radius = Math.floor(Math.min(step_x, step_y) / 2);
	ctx.arc((x + 0.5) * step_x, (y + 0.5) * step_y, radius/2, 0, 2*Math.PI, false);
	ctx.closePath();
	ctx.fill();

	ctx.fillStyle = tempColor;
}

function drawSnake(coordinates, isFriend) {
	/* Рисуем змейку */
	const friendSnake = '#c7737d';
	const enemySnake = '#4f4833';

	if (typeof(coordinates[0]) == 'stop')
		return;

	if (isFriend)
		ctx.fillStyle = friendSnake;
	else
		ctx.fillStyle = enemySnake;

    // {"test1": [[8, 8], [3, 6]]}
    let x_min = 0, x_max = 0
    let y_min = 0, y_max = 0

	for (let i = 0; i < coordinates.length - 1; i++)
	{
	    x_min = Math.min(coordinates[i][0], coordinates[i+1][0])
	    x_max = Math.max(coordinates[i][0], coordinates[i+1][0])
	    y_min = Math.min(coordinates[i][1], coordinates[i+1][1])
	    y_max = Math.max(coordinates[i][1], coordinates[i+1][1])
	 
	    for (let x = x_min; x <= x_max; x++)
            for (let y = y_min; y <= y_max; y++)
            {
		        drawSnakeElement(x , gameReplay.gameSettings.height - y - 1);
		    }
		//*/
    }
    drawSnakeHead(coordinates[0][0], gameReplay.gameSettings.height -  coordinates[0][1] - 1)

}


function drawGame() {
	/* Отрисовка одного кадра игры */
	if (gameStopped) return;

	drawFrame(frameCount);

	if ((frameCount === gameReplay.frames.length - 1 && frameStep === 1) ||
		(frameCount === 0 && frameStep === -1))
	{
		if (frameCount === gameReplay.frames.length - 1)
			frameCount = 0;
		stopButtonClick();
		return;
	}
	frameCount += frameStep;
}

function main() {
	canvas.width = width * step_x;
	canvas.height = height * step_y;
	document.getElementById("info_number").innerHTML = `${Object.keys(gameReplay.players).length}`;
	document.getElementById("info_map").innerHTML = `${gameReplay.gameSettings.weight}x${gameReplay.gameSettings.height}`;

	console.log("personalSnakeId = ", personalSnakeId);

	drawField();
	drawFrame(0);

	let timerId  = setTimeout(function timer() {
		drawGame();
		timerId  = setTimeout(timer, 500 / parseFloat(speedSelection.value));
		}, 500 / parseFloat(speedSelection.value));
}

main();

function drawFrame (numberFrame)
{
	let currentFrame = gameReplay.frames[numberFrame];
	document.getElementById("ReplayRange").value = numberFrame;

	drawField();

	for (let apple of currentFrame.apples)
		if (apple.length === 2)
			drawFood(apple[0], gameReplay.gameSettings.height - apple[1] - 1);
		else
			console.log(`Ошибка. Корд яблока - ${apple}`);

	let isFriend = null;
	for (let snake in currentFrame.snakes) {
		isFriend = snake === personalSnakeId;
		drawSnake(currentFrame.snakes[snake], isFriend);
	}
}