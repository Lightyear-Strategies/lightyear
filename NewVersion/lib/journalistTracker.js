let logoutVisible = false;
window.onload = () => {
    const profile = document.getElementById("profile");
    profile.addEventListener("click", () => {
        const logout = document.getElementById("logout");
        if (logoutVisible == false) 
            logout.style.visibility = "initial";
        else 
            logout.style.visibility = "hidden";
    
        logoutVisible = !logoutVisible
    })
}

function popupFunc() {
    var popup = document.getElementById("myPop");
    popup.classList.toggle("show");
}