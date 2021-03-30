// Связь с htm
const canvas  = document.getElementById("game_screen");
const ctx = canvas.getContext('2d');

let gameStopped = true;
const btnStop  = document.getElementById("stop");
btnStop.addEventListener("click", stopButtonClick);

// Карта Игры
const height = 32;
const width = 48;

let step_x = Math.floor(canvas.width / width);
let step_y = Math.floor(canvas.height / height);

canvas.width = width * step_x;
canvas.height = height * step_y;

/* Наброски
const map = new Array(height);
for (let i = 0; i < height; i++)
	map[i] = new Array(width); 
*/


function drawField() {
	/* Рисуем поле */
	ctx.fillStyle = "#8cca88";
	ctx.fillRect(0, 0, canvas.width, canvas.height);
	
	// ?
	ctx.strokeStyle = "#77b373";
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
	ctx.fillRect(x * step_x, y * step_y, step_x, step_y);  
}

function drawSnakeHead(x, y) {
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

function drawSnake() //  user_id, snakeCoordinates
{
	let isFriend = false;
	if (true) // TODO: Добавить проверку на пользователя
		isFriend = true;
	
	const friendSnake = '#57ff64';
	const enemySnake = '#f64d27';

	if (isFriend)
		ctx.fillStyle = friendSnake;
	else
		ctx.fillStyle = enemySnake;
	
	//
	drawSnakeHead(1, 1, isFriend);
	drawSnakeElement(2, 1, isFriend);
	drawSnakeElement(3, 1, isFriend);
	drawSnakeElement(4, 1, isFriend);
}

function stopButtonClick() {
	if (gameStopped) {
		btnStop.value = "Остановить";
	} else {
		btnStop.value = "Запуск";
	}
	gameStopped = !gameStopped;
}

function drawGame() {
	if (gameStopped) return;
	
	// получить данные кадра
	// ...
	
	let command = gameReplay[stepCount];
	let command_context = "";

	// отрисовака кадра
	drawField();

	if (command == "s") {
		drawSnake(); 
	} else if (command == "a") {
		drawFood(3 + stepCount,3 + stepCount);
	}
	
	// ...
	if (stepCount < maxStep - 1) stepCount += 1;
}

function main(){
	drawField();
	drawFood(0,0);
	drawFood(width - 1, height - 1);
	
	let game = setInterval(drawGame, 1000);
}

gameReplay = "sa";
let maxStep = gameReplay.length;
let stepCount = 0;

main();

