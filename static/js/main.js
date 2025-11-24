

const closeBtn = document.querySelector("aside i#close-btn");

closeBtn.addEventListener("click" , (e) => {
    e.target.parentElement.classList.toggle("active");
})

// Active Link In The Side Bar
const links = document.querySelectorAll("aside li a");

links.forEach((e) => {
    if (e.getAttribute("href").replace("/", "") === window.location.href.split("/")[window.location.href.split("/").length - 1]) {
        e.parentElement.classList.add("active");
    }
})