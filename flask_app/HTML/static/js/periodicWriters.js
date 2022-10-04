let currentFile = null;
let toastAppear = false;

const addListeners = () => {
    // File Picker/Drop Zone
    const drop = document.getElementById("drop_zone");
    const filePicker = document.getElementById("file")
    // Modal Listener
    const instruction = document.querySelector(".instructionBtn");
    const modalBtn = document.querySelector("#modalBtn");

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
                        currentFile = file;
                        addFile(currentFile);
                    } else {
                        toast("error", file.name + " is not of the type .csv, please drop a appropriate file.");
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
        currentFile = event.target.files;
        addFile(currentFile);
        this.value = "";
    })

    /* Up Button */
    const upBtn = document.querySelector("#upBtn");
    upBtn.addEventListener("click", () => {
        window.scrollTo(0, 0);
    })

    instruction.addEventListener("click", () => {
        document.querySelector(".modal").style.visibility = "visible";
        document.querySelector("body").style.overflowY = "hidden";
    })

    modalBtn.addEventListener("click", () => {
        document.querySelector(".modal").style.visibility = "hidden";
        document.querySelector("body").style.overflowY = "inherit";
    })
}

// Trigger when drop file, add a file that can be deleted
const addFile = (currentFile) => {
    const fileLocation = document.querySelector("#fileSelected");
    const fileChild = document.createElement("h2");
    if (fileLocation.children.length > 0) {
        fileLocation.removeChild(fileLocation.lastChild);
    }

    if (currentFile.length == 1) {
        fileChild.innerHTML = currentFile[0].name;
    } else {
        fileChild.innerHTML = currentFile.name;
    }
    fileLocation.appendChild(fileChild);
}

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

// Cookies