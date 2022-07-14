
let currentFile = null;
let toastAppear = false;

// Toast | Maybe change the text color of Toast
const toast = (type, text) => {
    if (toastAppear == true) return;

    const toast = document.querySelector(".toast");
    const toastLoader = document.querySelector(".toast-loader");
    const toastText = document.querySelector(".toast-content > h2");

    toast.style.visibility = "visible";
    toastLoader.style.visibility = "visible";
    toastText.innerHTML = text;
    toastLoader.style.transition = "linear width 1.2s";
    toastAppear = true;

    if (type == "error") 
        toastLoader.style.backgroundColor = "var(--lightyear-red)";
    else if (type == "info") 
        toastLoader.style.backgroundColor = "var(--lightyear-blue)";
    else
        toastLoader.style.backgroundColor = "var(--lightyear-yellow)"

    setTimeout(() => {
        toastLoader.classList.add("toast-loader-end");
    }, 200);

    setTimeout(() => {
        toast.style.visibility = "hidden";
        toastLoader.style.visibility = "hidden";
        toastLoader.style.transition = "none";
        toastLoader.classList.remove("toast-loader-end")
        toastAppear = false;
    }, 1500);
}


// Loader Loading
const load = () => {
    let loader = document.querySelector("#loader"); 
    setTimeout(() => {
        loader.style.transform = "translateY(-100%)"; 
        document.querySelector("body").style.overflowY = "inherit";
    }, 1000);
}



window.onscroll = () => {
    if (window.scrollY > 0)
        document.querySelector('#upBtn').style.opacity = "1";
    else
        document.querySelector("#upBtn").style.opacity = "0";
}

window.onload = () => {
    document.querySelector(".toast").style.visibility = "hidden";
    document.querySelector(".toast-loader").style.visibility = "hidden";
    document.querySelector("body").style.overflowY = "hidden";
    load();
    document.querySelector("#upBtn").style.opacity = "0";
    addListeners();
}