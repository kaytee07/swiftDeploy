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

function actionOnContainer(action, id){
    console.log(action)
    console.log(id)
    const requestOptions = {
	method: "POST",
	headers: {
	    "Content-Type": "application/json",
	}
    };

    let url = `http://localhost:5001/api/v1/containers/${action}/${id}`

    
    fetch(url, requestOptions)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
	    window.location.reload();

    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}

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
               <h5 class="id">${value.image_id}</h5>
               <h5>${value.status}</h5>
               <button class="start">${value.status === "running" ? "stop" : "start"}</button>
               <button class="open">Open</button>
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

const getlist = document.querySelector('.containers')
const startBtn = document.querySelector("button")
console.log(getlist)
getlist.addEventListener("click", function(event) {
  if (event.target.classList.contains("start")) {
    const buttonText = event.target.textContent;
      let container_id = event.target.parentElement.children[1].innerText;
      actionOnContainer(buttonText, container_id);
      event.stopPropagation();
  }else if (event.target.classList.contains("stop")) {
      const buttonText = event.target.textContent;
      let container_id = event.target.parentElement.children[1].innerText;
      actionOnContainer(buttonText, container_id);
      event.stopPropagation();
  }
});
