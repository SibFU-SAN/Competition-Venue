function chooseGame(){
	document.getElementById("game_id").value = "32";
	console.log(sessionList);
}

//const game_id = document.getElementById("game_id");
//game_id.addEventListener("click", reverseButtonClick);

//let sessionList = JSON.parse(``);
let sessionList = [
{
	id: 131232,
	map: [10, 100],
	gamers: [5, 20],
	date: "this date",
	duration: 34,
},
{
	id: 243534,
	map: [10, 100],
	gamers: [5, 20],
	date: "this date",
	duration: 34,
}
];

let template = `
	<div class="session">
		<div class="session-head"> <!-- Загаловок -->
			<h3>ID: <span>23112</span></h3>
			<input type="button" value="Выбор" class="btn" onclick="chooseGame()">
		</div>
		<div class="session-info"> <!-- Информаця о игре -->
			<ul>
				<li>Колво участников: <span>44</span></li>
				<li>Размер карты: <span>44x44</span></li>
			</ul>
			<ul>
				<li>Дата начала: <span>10.10.2021</span></li>
				<li>Длительность: <span>45 min</span></li>
			</ul>
		</div>
	</div>
	`;

function main()
{
	document.createElement(template);
}

main();