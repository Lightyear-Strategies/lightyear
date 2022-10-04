window.onload = () => {
    const back = document.querySelector(".goBack");
    back.addEventListener("click", () => {
        history.back();
    })
}