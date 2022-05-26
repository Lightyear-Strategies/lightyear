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
                    recieved : "3/23",
                    summary : "Seeking a financial planner who works with six-figure earners",
                    query: "I am looking for a financial planner who frequently works with six-figure earners about money routines that keep them wealthy?My DM's are open. Much appreciated!",
                    requirements : "Name, title, company you work for, and contact information",
                    company : "Business Insider",
                    category : "Business and Finance",
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
    
    element_component = document.createElement("button");
    element_component.classList.add("expandable");
    
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