const REPORTERS_PER_PAGE = 10;
reporter_wrapper = document.getElementById("reporter_wrapper")


const reporters = getReporters();



displayReporters(0,10);



function getReporters() {
    output = [];
    for (let i = 0; i<20; i++) { //placeholder, use whatever you neeed to get that reporter data here into the format shown by this object
        output.push(
            
                {
                    name : "John Doe",
                    email : "john@blockbuster.com",
                    deadline : "4/15",
                    query: "Peter, I need ten emo bitches and they all need to be bad",
                    content : "Blah blah blah. Reporter reporter reporter",
                    selected : false
                }
        )
    }
    return output;
}



function displayReporters(min,max) {
    const reporter_wrapper= document.getElementById("reporter_wrapper")
    console.log(reporter_wrapper);
    reporter_wrapper.innerHTML  = ""; 
    for (let i = min; i<(max+1); i++) {
        insert_reporter(reporters[i]);
    }
}

function insert_reporter(reporter_i) {
    const table_element = document.createElement("div");
    table_element.classList.add("table-element");
    let element_component;
    for (property in reporter_i) {
        element_component = document.createElement("div");

        if (property != 'selected') {
            if (property == 'deadline') element_component.innerHTML = "Deadline: "
            element_component.innerHTML = element_component.innerHTML + reporter_i[property];

            element_component.classList.add(property);
        }

        else {
            element_component.classList.add('selection-indicator');
            if (reporter_i['selected']){
                element_component.classList.add('selected');
            }
            else {
                element_component.classList.add('not-selected');
            }
        }
        
        table_element.appendChild(element_component);
    }
    document.createElement('div')
    reporter_wrapper.appendChild(table_element);
}