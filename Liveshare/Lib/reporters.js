
const addListeners = () => {
    // File Picker/Drop Zone
    const drop = document.getElementById("drop_zone");
    const filePicker = document.getElementById("filepicker")

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
    })

    /* Up Button */
    const upBtn = document.querySelector("#upBtn");
    upBtn.addEventListener("click", () => {
        window.scrollTo(0, 0);
    })
}

const load = () => {
    loader = document.querySelector("#loader"); 
    setTimeout(() => {
        loader.style.transform = "translateY(-100%)"; 
        document.querySelector("body").style.overflow = "inherit";
    }, 700);
}


window.onscroll = () => {
    if (window.scrollY > 0)
        document.querySelector('#upBtn').style.opacity = "1";
    else
        document.querySelector("#upBtn").style.opacity = "0";
}

window.onload = () => {
    document.querySelector("body").style.overflow = "hidden";
    load();
    document.querySelector("#upBtn").style.opacity = "0";
    addListeners();
}