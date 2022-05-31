
const REPORTER_WRAPPER= document.getElementById("reporter_wrapper");
const REPORTERS = getReporters();

displayReporters();

function getReporters() {
    output = [];
    for (let i = 0; i<1; i++) { //placeholder, use whatever you neeed to get that reporter data here into the format shown by this object
        output.push(
            
                {
                    name : "Yitzi Weiner & Martita Mestey",
                    email : "query-do04@helpareporter.net",
                    deadline : "4/15",
                    recieved : "3/23",
                    summary: "5 Things You Need To Create A Highly Successful Career As A Public Relations Pro",
                    query : "Dear FriendsAuthority Magazine is starting a new series called5 Things You Need To Create A Highly Successful Career In PublicRelationsHave you seen the show Flack? Ever think of pursuing a real lifecareer in PR? What does it take to succeed in PR? What are thedifferent forms of Public Relations? Do you have to have acollege degree in PR? How can you create a highly lucrativecareer in PR? In this interview series, we would like to interview successfulpublicists and Public Relations pros, who can share stories andinsights from their experience about \"5 Things You Need ToCreate A Highly Successful Career In Public Relations.\"All of the full interviews will be published in AuthorityMagazine and they will look similar to the following:https://medium.com/authority-magazine/search?q=Publicist%20Rockstars",                    
                    requirements : "Name, title, company you work for, and contact information",
                    company : "Business Insider",
                    industry : "Business and Finance",
                    requirements : "In this interview series, we would like to interview successfulpublicists and Public Relations pros, who can share stories andinsights from their experience about \"5 Things You Need ToCreate A Highly Successful Career In Public Relations.\"",
                    selected : false
                }
        )
        output.push( {
                summary : "neurologist re: aphasia",
                name : "Heidi Godman",
                email : "query-dr2r@helpareporter.net",
                query : "	I need a neurologist or a neuropsychologist from a large USacademic hospital, not in California, who can talk to me aboutaphasia. (Already have 2 experts from CA)",
                requirements : "-Must be someone who frequently deals with people who haveaphasia. -Must be from a large academic hospital. -Cannot be anyone from California-- I already have two expertsfrom there. -Thank you everyone for being so helpful! Sorry I can't useeveryone in these articles.",
                recieved : "5/3",
                deadline : "6/21",
                company :  "US News and World Report",
                industry : "Biotech and Healthcare",
                selected : true
            }
        )
    }
    return output;
}

function displayReporters() { // for now it just displays the first 10 
    for (let reporter of REPORTERS) {
        insert_reporter(reporter);
    }
}

function std_make(class_name, parent, ops) { // ops = optional parameters: ops.content, ops.tag
    if (ops == undefined ) ops = {
        content: '',
        tag: 'div',
        grid_child: true
    }
    if (ops.content == undefined ) ops.content = "";
    if (ops.tag == undefined ) ops.tag = 'div'
    if (ops.grid_child == undefined) ops.grid_child = true;

    const doc_element = document.createElement(ops.tag);
    doc_element.classList.add(class_name);
    doc_element.innerHTML = ops.content;
    if (ops.grid_child) doc_element.style['grid-area'] = class_name;
    parent.appendChild(doc_element);

    return doc_element
}

function insert_reporter(r) {
    

    //root wrapper and first children
    const wrapper = std_make('wrapper',REPORTER_WRAPPER, {grid_child: false});
    const bar = std_make('selector-indicator', wrapper, {grid_child: false});
    if (r['selected']) bar.classList.add('selected-true');
    const reporter = std_make('reporter-grid',wrapper, {grid_child: false})
    

    //wrappers for grid elements
    const name_email_wrapper = std_make('name-email-wrapper', reporter);
    const query_wrapper = std_make('query-wrapper',reporter);
    const requirements_wrapper = std_make('requirements-wrapper',reporter);
    const summary_industry_company_wrapper = std_make('summary-industry-company-wrapper',reporter);
    const industry_company_wrapper = std_make('industry-company-wrapper',summary_industry_company_wrapper, {grid_child: false});

    //misc wrapper children
    const query_header = std_make('query-header',query_wrapper, {content:"Query: ", grid_child: false})
    const requirements_header = std_make('requirements-header',requirements_wrapper, {content:"Requirements: ", grid_child: false})

    //data to display
    const summary = std_make('summary',summary_industry_company_wrapper,{content: r['summary'], grid_child: false})
    const name = std_make('name',name_email_wrapper,{content: r['name'], grid_child: false})
    const email = std_make('email',name_email_wrapper,{content: r['email'], grid_child: false})
    const query = std_make('query',query_wrapper, {content:r['query'], grid_child: false})
    const requirements = std_make('requirements',requirements_wrapper,{content:r['requirements'], grid_child: false})
    const recieved = std_make('recieved',reporter,{
        content:("Recieved: " + r['recieved'])
    })
    const deadline = std_make('deadline',reporter,{
        content:("Deadline: "+ r['deadline'])
    })
    const industry = std_make('industry',industry_company_wrapper,{content:r['industry'], grid_child: false})
    const company = std_make('company',industry_company_wrapper,{content:r['company'], grid_child: false})
    
    //for our expand button
    const include_when_expanded = [
        name_email_wrapper, query_wrapper, requirements_wrapper, name, email, query, requirements, query_header, requirements_header
    ];
    for (let element of include_when_expanded) {
        element.classList.add('include-when-expanded')
    }

    //expand button
    make_expand_button(reporter,include_when_expanded)

    //"Add button"
    let str;
    if (r['selected']) str = 'Remove'
    else str = 'Add'
    const add_button = std_make('add-button',reporter,{
        content: str, 
        tag:'button',
        grid_child:true})
    add_button.onclick = function() {
        if (this.innerHTML == "Add") {
            this.innerHTML = "Remove"
        } else {
            this.innerHTML = "Add"
        }
        bar.classList.toggle('selected-true')
    }
    

    REPORTER_WRAPPER.appendChild(wrapper);
}

function make_expand_button(parent, include_when_expanded){
    const expand_button = std_make('expand-button', parent, {tag: 'button'});
    const expand_arrow = std_make('expand-arrow',expand_button,{tag: 'img', grid_child: false});
    const expand_text = std_make('expand-text',expand_button, {grid_child: false} )

    expand_arrow.src = 'assets/Images/expand_arrow.svg';
    expand_text.innerHTML = 'Show more';

    
    expand_button.onclick = function () {
        if (!parent.classList.contains('expanded-true')) { //collapse
            expand_text.innerHTML = 'Show less';
            expand_arrow.src = 'assets/Images/collapse_arrow.svg';
        } else {
            expand_text.innerHTML = 'Show more';
            expand_arrow.src = 'assets/Images/expand_arrow.svg';
        }
        parent.classList.toggle('expanded-true')
        for (let member of include_when_expanded) {
            member.classList.toggle('include-when-expanded');
        }
    }
}