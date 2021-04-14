// Данные Зрителя
const accountHesh = 1;
let personalSnakeId = null;

// Данные Игроков: Hesh <=> Name
//const playersHesh = JSON.parse(``);

// Карта Игры
const gameReplay = JSON.parse(`
	{
		"players": {
			"29437191": 1,
			"77539713": 0
			},
		"gameSettings": {
			"height": 50,
			"weight": 100
			},
		"frames": [
			{ "apples": [ [ 7, 2 ], [ 2, 2 ], [ 2, 7 ], [ 7, 7 ] ], "snakes": { "29437191": [ [ 4, 3 ], [ 3, 3 ] ], "77539713": [ [ 4, 4 ], [ 4, 5 ] ] } },
			{ "apples": [ [ 7, 2 ], [ 2, 2 ], [ 2, 7 ], [ 7, 7 ] ], "snakes": { "29437191": [ [ 5, 3 ], [ 4, 3 ] ], "77539713": [ "stop" ] } },
			{ "apples": [ [ 7, 2 ], [ 2, 2 ], [ 2, 7 ], [ 7, 7 ] ], "snakes": { "29437191": [ [ 6, 3 ], [ 5, 3 ] ], "77539713": [ "stop" ] } },
			{ "apples": [ [ 7, 2 ], [ 2, 2 ], [ 2, 7 ], [ 7, 7 ] ], "snakes": { "29437191": [ [ 7, 3 ], [ 6, 3 ] ], "77539713": [ "stop" ] } },
			{ "apples": [ [ 2, 2 ], [ 2, 7 ], [ 7, 7 ] ], "snakes": { "29437191": [ [ 7, 2 ], [ 7, 3 ] ], "77539713": [ "stop" ] } },
			{ "apples": [ [ 2, 2 ], [ 2, 7 ], [ 7, 7 ] ], "snakes": { "29437191": [ [ 6, 2 ], [ 7, 2 ], [ 7, 3 ] ], "77539713": [ "stop" ] } }
			]
	}
`);

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
	if (frameStep == 1)
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

	drawSnakeHead(coordinates[0][0] - 1, coordinates[0][1] - 1)
	for (let i = 1; i < coordinates.length; i++)
		drawSnakeElement(coordinates[i][0] - 1, coordinates[i][1] - 1);
}


function drawGame() {
	/* Отрисовка одного кадра игры */
	if (gameStopped) return;
	
	drawFrame(frameCount);
	
	if ((frameCount == gameReplay.frames.length - 1 && frameStep == 1) || 
		(frameCount == 0 && frameStep == -1))
	{
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

	// Нахождение нужного id
	for (let i in gameReplay.players) {
		if (gameReplay.players[i] == accountHesh)
			personalSnakeId = i;
	}
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
		if (apple.length = 2)
			drawFood(apple[0] - 1, apple[1] - 1);
		else
			console.log(`Ошибка. Корд яблока - ${apple}`);

	let isFriend = null;
	for (let snake in currentFrame.snakes) {
		if (snake == personalSnakeId)
			isFriend = true;
		else
			isFriend = false;
		drawSnake(currentFrame.snakes[snake], isFriend);
	}
}