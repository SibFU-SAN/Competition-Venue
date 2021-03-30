/* Размеры поля в клетках */
let height = 32;
let width = 48;

const map = new Array(height);
for (let i = 0; i < height; i++)
	map[i] = new Array(width);

const canvas  = document.getElementById("game_screen");
const ctx = canvas.getContext('2d');

function drawField() {
	/* Рисуем поле */
	let step;
	
	ctx.fillStyle = "#abff96";
	ctx.fillRect(0, 0, canvas.width, canvas.height);
	
	ctx.fillStyle = "#000000";
	
	step = Math.floor(canvas.width / width);
	for (j = step; j < canvas.width; j += step) {
		ctx.beginPath();
		ctx.moveTo(j, 0);  
		ctx.lineTo(j, canvas.height);
		ctx.closePath();
		ctx.stroke();
	}
	
	step = Math.floor(canvas.height / height);
	for (j = step; j < canvas.height; j += step) {
		ctx.beginPath();
		ctx.moveTo(0, j);  
		ctx.lineTo(canvas.width, j);
		ctx.closePath();
		ctx.stroke();
	}
}

function drawFood(x, y) {
	/* Рисуем еду */
	let step_x = Math.floor(canvas.width / width);
	let step_y = Math.floor(canvas.height / height);
	let radius = Math.floor(Math.min(step_x, step_y) / 2);

	ctx.fillStyle = '#ff9090';
	ctx.beginPath();
	ctx.arc((x + 0.5) * step_x, (y + 0.5) * step_y, radius, 0, 2*Math.PI, false);
	ctx.closePath();
	ctx.fill();
}


function drawGame() {
	/* Нарисовать поле */
	drawField();

	/* Пройтись по массиву, отображая каждый элемент */
	drawFood(5, 5);

	/* Взять следующий "кадр" */
}

drawGame();

//let game = setInterval(drawGame, 500);
