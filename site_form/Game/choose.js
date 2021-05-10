//let elementsOfList = JSON.parse(json_str);
let elementsOfList = [
{
	game_id: 131232,
	map: [70, 90],
	players: 5,
	datestart: "12321321",
	duration: 34,
},
{
	game_id: 243534,
	map: [100, 100],
	players: 20,
	datestart: "312312",
	duration: 34,
}];

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
		var fragment = createTemplate(i.game_id, i.map, i.players, i.datestart, i.duration);
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