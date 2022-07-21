let open = false;

window.onresize = () => {
    const aside = document.querySelector("aside");
    const hamburgerIcon = document.querySelector("#hamIcon");
    const closeIcon = document.querySelector("#closeIcon");
    if (window.innerWidth >= 1900) {
        aside.style.display = "none";
        hamburgerIcon.style.display = "initial";
        closeIcon.style.display = "none"
        open = false;
    }
}

window.onload = () => {
    const aside = document.querySelector("aside");
    const hamburgerIcon = document.querySelector("#hamIcon");
    const closeIcon = document.querySelector("#closeIcon");

    hamburgerIcon.addEventListener('click', () => {
        if (open == false) {
            aside.style.display = "initial";
            hamburgerIcon.style.display = "none";
            closeIcon.style.display = "initial"
            open = true;
        } 
    })

    closeIcon.addEventListener('click', () => {
        if (open == true) {
            aside.style.display = "none";
            hamburgerIcon.style.display = "initial";
            closeIcon.style.display = "none"
            open = false;
        }
    })
};