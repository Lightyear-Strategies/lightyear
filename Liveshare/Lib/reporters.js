let list = [];
let testing = 1;

const addListeners = () => {
    // File Picker/Drop Zone
    const drop = document.getElementById("drop_zone");
    const filePicker = document.getElementById("file")

    // Drag over and drag leave are completely optional
    drop.addEventListener("dragover", (event) => {
        event.preventDefault();
        console.log("Over");
    });

    drop.addEventListener("dragleave", () => {
        console.log("Leave");
    });

    // When you drop the files
    drop.addEventListener("drop", (event) => {
        event.preventDefault();
        if(event.dataTransfer.items) {
            for (let i = 0; i < event.dataTransfer.items.length; i++) {
                const element = event.dataTransfer.items[i];
                if (element.kind === 'file') {
                    let file = element.getAsFile();
                    //  If the following CSV or NOT
                    if (file.type === "text/csv"){
                        console.log("Got Image");
                        addFile();
                    }
                }
            }
        } else {
            for (let i = 0; i < event.dataTransfer.files.length; i++) {
                console.log("B");
            }
        }
    });

    filePicker.addEventListener("change", (event) => {
        console.log(filePicker.value);
        addFile();
        this.value = "";
    })

    /* Up Button */
    const upBtn = document.querySelector("#upBtn");
    upBtn.addEventListener("click", () => {
        window.scrollTo(0, 0);
    })
}

// Trigger when drop file, add a file that can be deleted
const addFile = () => {
    let fileLocation = document.querySelector("#fileSelected");
    let fileChild = document.createElement("h2");
    fileChild.innerHTML = testing;
    fileLocation.appendChild(fileChild);
    testing++;
    console.log(fileLocation.children);
}

// Error Issue
const toast = (type, text) => {
    const toast = document.querySelector(".toast");
    const toastLoader = document.querySelector(".toast-loader");
    const toastText = document.querySelector(".toast-content > h2");

    toast.style.visibility = "visible";
    toastLoader.style.visibility = "visible";
    toastText.innerHTML = text;

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
        toastLoader.classList.remove("toast-loader-end")
    }, 1400);
}


// Loader Loading
const load = () => {
    loader = document.querySelector("#loader"); 
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