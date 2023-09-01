const pullbtn = document.querySelector(".pull_cont button")
const closebtn = document.querySelector("svg")
const card = document.querySelector(".pull_card")

pullbtn.addEventListener('click', () => {
  card.style.display = 'flex';
});

closebtn.addEventListener('click', () => {
  card.style.display = 'none';
});
