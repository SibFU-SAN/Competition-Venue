let json_str = `[{
	"gameID": 1432423,
	"players": 46,
	"gameSettings": {
		"height": 100,
		"weight": 100
		},
	"dateStart": 22464,
	"duration": 45
	},
	{
	"gameID": 243324,
	"players": 10,
	"gameSettings": {
		"height": 70,
		"weight": 70
		},
	"dateStart": 1132,
	"duration": 60
	}]`;

let elementsOfList = JSON.parse(json_str);

/* 
{
"gameID": 1432423,
"players": 10,
"gameSettings": {
	"height": 50,
	"weight": 100
	},
"dateStart": 1132,
"duration": 45
}
*/

function createTemplate(game_id, mapSize, NumberOfPlayers, startDate, duration) {
	let template = `
		<div class="session">
			<div class="session-head">
				<h3>ID: <span>${game_id}</span></h3>
				<input type="button" value="Выбор" class="btn" data-number="${game_id}">
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

function chooseGame(game_id){
	document.getElementById("game_id").value = game_id;
	let form = document.getElementById("form");
	form.submit();
}

function addElements(list, listDOMId) {
	// Добавление новых элементов
	for (let i of list)
	{
		var fragment = createTemplate(i.gameID, [i.gameSettings.weight, i.gameSettings.height], i.players, i.dateStart, i.duration);
		document.getElementById(listDOMId).appendChild(fragment);
	}

	// Добавление событие по нажатию
	const tabs = document.querySelectorAll(".btn");
	tabs.forEach(function(item) { 
		item.addEventListener("click", function() {
			let currentBtn = item;
			let game_id = currentBtn.getAttribute("data-number");
			
			chooseGame(game_id);
		});
	});
}

addElements(elementsOfList, "session_list");