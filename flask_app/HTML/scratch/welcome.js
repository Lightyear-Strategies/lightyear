let curSlide;
let maxSlide;

document.addEventListener('scroll', () => {
    const header = document.querySelector("header");

    if (scrollY == 0) {
        header.style.backgroundColor = "#ffffff";
        document.getElementById("strat").style.color = "#F04C23";
        for (i = 1; i < 4; i ++) {
            document.getElementById("a-" + i).style.color = "#F04C23";
        }
    } else {
        header.style.backgroundColor = "#FCE300";
        document.getElementById("strat").style.color = "#ffffff";
        for (i = 1; i < 4; i ++) {
            document.getElementById("a-" + i).style.color = "#ffffff";
        }
    }
    
    let cards = document.querySelectorAll(".cards");
    for (i = 0; i < cards.length; i ++) {
        if (cards[i].clientHeight < scrollY - 800) {
            cards[i].classList.add("animate__animated", "animate__fadeInUp");
        }
    }
});

window.onload = () => {
    /*
    const slides = document.querySelectorAll(".slide");

    curSlide = 0;
    maxSlide = slides.length - 1;

    slides.forEach((slide, index) => {
        slide.style.transform = `translateX(${index * 100}%)`;
    })

    const nextSlide = document.querySelector(".btn-next");
    nextSlide.addEventListener("click", () => {
        if(curSlide === maxSlide) 
            curSlide = 0;
        else
            curSlide++;

        slides.forEach((slide, index) =>{
            slide.style.transform = `translateX(${100 * (index - curSlide)}%)`;
        })
    })

    const prevSlide = document.querySelector(".btn-prev");

    prevSlide.addEventListener("click", () => {
        if (curSlide === 0) {
            curSlide = maxSlide;
        } else {
            curSlide--;
        }

        slides.forEach((slide, index) =>{
            slide.style.transform = `translateX(${100 * (index - curSlide)}%)`;
        })
    })
    */
};