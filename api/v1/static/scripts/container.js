const pullbtn = document.querySelector(".pull_cont button")
const closebtn = document.querySelector("svg")
const card = document.querySelector(".pull_card")
const containerList = document.querySelector("ul.containers")



pullbtn.addEventListener('click', () => {
  card.style.display = 'flex';
});

closebtn.addEventListener('click', () => {
  card.style.display = 'none';
});


function getAllContainers(usernme) {
fetch(`http://localhost:5001/api/v1/containers/${usernme}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
	let html = ""
	const containers = Object.entries(data)
	for (const [key, value] of containers) {
	 html+= `
               <li class="container">
               <h5>${value.name}</h5>
               <h5>${value.container_id}</h5>
               <h5>${value.status}</h5>
               <button>${value.status === "stopped" ? "start" : "stop"}</button>
               <button>Open</button>
               </li>
               `;  
	}
	if (html) {
	   containerList.innerHTML = html
	}
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}

getAllContainers(username)

