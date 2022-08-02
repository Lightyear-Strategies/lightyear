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

// Pop-up
function popupFunc() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
}

// Add and Copy Link to Clipboard -- need to test
async function copyLinkToClipboard(){ // only copies the text
    await navigator.clipboard.writeText(document.getElementById('copyLink').value);
}

async function addLinkToClipboard(){
    var addText = await navigator.clipboard.readText();
    addText+= ", "+ document.getElementById('addLink').value;
    await navigator.clipboard.writeText(addText);
    console.log(addText);
}

// Add and Copy Brief to Clipboard -- need to test
async function copyBriefToClipboard(){ // only copies the text
    await navigator.clipboard.writeText(document.getElementById('copyBrief').value);
}

async function addBriefToClipboard(){
    var addText = await navigator.clipboard.readText();
    addText+= ", "+ document.getElementById('addBrief').value;
    await navigator.clipboard.writeText(addText);
    console.log(addText);
}

function search() {

}

// Removing Follower
function remove(el) {
    var element = el;
    element.parentElement.remove();
}

// Slider Gradient Change
function dynamicSlider() {
    var slider = document.getElementById("myRange");
    if (slider.value == 1) {
        slider.style.background = "linear-gradient(18.03deg, rgba(197, 28, 224, 0.996446) 4.12%, #AC5D73 13.65%, #A800C4 15.51%, #0085FF 99.61%)";
    }
    else if (slider.value > 1 && slider.value <= 2) {
        slider.style.background = "linear-gradient(82.9deg, rgba(197, 28, 224, 0.996446) 34.6%, #AC5D73 39.54%, #A800C4 49.34%, #0085FF 81.6%)";
    }
    else if (slider.value > 2 && slider.value <= 3) {
        slider.style.background = "linear-gradient(275.16deg, rgba(197, 28, 224, 0.996446) 7.94%, rgba(160, 67, 175, 0.996446) 30.47%, #2295FF 51.08%, #A800C4 76.26%)";
    }
    else {
        slider.style.background = "linear-gradient(268.61deg, rgba(197, 28, 224, 0.996446) 5.78%, #AC5D73 16.08%, #A800C4 36.5%, #0085FF 103.73%)";
    }
}
