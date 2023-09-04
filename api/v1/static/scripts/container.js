const pullbtn = document.querySelector(".pull_cont button")
const closebtn = document.querySelector("svg")
const card = document.querySelector(".pull_card")


pullbtn.addEventListener('click', () => {
  card.style.display = 'flex';
});

closebtn.addEventListener('click', () => {
  card.style.display = 'none';
});

console.log(id)
console.log(username)


fetch(`http://localhost:5001/api/v1/containers/${username}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
