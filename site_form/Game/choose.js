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
	gamers: 5,
	date: "this date",
	duration: 34,
},
{
	id: 243534,
	map: [10, 100],
	gamers: 20,
	date: "this date",
	duration: 34,
}
];


function createTemplate(game_id, NumberOfPlayers, mapSize, startDate, duration) {
	let template = `
		<div class="session">
			<div class="session-head">
				<h3>ID: <span>${game_id}</span></h3>
				<input type="button" value="Выбор" class="btn" onclick="chooseGame()">
			</div>
			<div class="session-info">
				<ul>
					<li>Колво участников: <span>${NumberOfPlayers}</span></li>
					<li>Размер карты: <span>${mapSize[0]}x${mapSize[1]}</span></li>
				</ul>
				<ul>
					<li>Дата начала: <span>${startDate}</span></li>
					<li>Длительность: <span>${duration} min</span></li>
				</ul>
			</div>
		</div>
		`;
    var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
    temp.innerHTML = template;
    while (temp.firstChild) {
        frag.appendChild(temp.firstChild);
    }
    return frag;
}

function main()
{
	for (i of sessionList)
	{
		var fragment = createTemplate(1111, 44, [50, 100], "13.23.22", 50);
		document.getElementById("session_list").appendChild(fragment);
	}
}

main();