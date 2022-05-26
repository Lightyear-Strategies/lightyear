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