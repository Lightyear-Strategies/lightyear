const INCLUDE_WHEN_EXPANDED = ['name','email','query','requirements'];
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
                industry : "Biotech and Healthcare"
            }
        )
    }
    return output;
}

function displayReporters() { // for now it just displays the first 10 
    REPORTER_WRAPPER.innerHTML  = ""; 
    for (let reporter of REPORTERS) {
        insert_reporter(reporter);
    }
}

function std_make(name, parent, content = "", grid_child = true, tag = 'div') {
    const doc_element = document.createElement(tag);
    doc_element.classList.add(name);
    doc_element.innerHTML = content;
    if (grid_child) doc_element.style['grid-area'] = name;
    parent.appendChild(doc_element);

    return doc_element
}

function insert_reporter(reporter_i) {
    const wrapper = std_make('wrapper',REPORTER_WRAPPER);
    const reporter = std_make('reporter-grid',wrapper)

    const bar = document.createElement('selector-indicator',reporter);
    if (reporter_i['selected']) bar.classList.add('selected-true');

    const name_email_wrapper = std_make('name-email-wrapper',reporter);
    const industry_company_wrapper = std_make('industry-company-wrapper',reporter);

    let wrapped_members_object = {
        name : wrapper,
        email: wrapper,
        industry: wrapper,
        company: wrapper
    };
    const wrapped_members = ['name','email','industry','company'];

    const include_when_expanded = [];
    let reporter_member;
    const query_wrapper = std_make('query-wrapper',reporter);
    const requirements_wrapper = std_make('requirements-wrapper',reporter);

    const query_pre = std_make('query-pre',query_wrapper);
    const query_content = std_make('query-content',query_wrapper);
    
    const requirements_pre = std_make('requirements-pre',requirements_wrapper);
    const requirements_content = std_make('requirements-content',requirements_wrapper);

    for (property in reporter_i) {
        reporter_member = document.createElement("div");
        reporter_member.classList.add(property);

        if (property == 'selected') continue; //selected gets its own div

        if (property == 'deadline' ) { //content handling
            reporter_member.innerHTML = "Deadline: " + reporter_i[property];
        } else if (property == 'recieved') {
            reporter_member.innerHTML = "Recieved: " + reporter_i[property];
        } else if (property == 'requirements') {
            
            reporter_member.innerHTML = "<span>Requirements:<span/><br>" + reporter_i[property];
        } else if (property == 'query') {
            reporter_member.appendChild()
        } else {
            reporter_member.innerHTML = reporter_i[property];
        }

        if (wrapped_members.includes(property)) { //theses are the ones we're going to wrap in dividers before placing in the grid.
            wrapped_members_object[property] = reporter_member;
        } else reporter.appendChild(reporter_member); 

        reporter_member.style['grid-area'] = property;
        if (INCLUDE_WHEN_EXPANDED.includes(property)) {
            reporter_member.classList.add('include-when-expanded')
            include_when_expanded.push(reporter_member);
        }
    }

    industry_company_wrapper.appendChild(wrapped_members_object['industry']);
    industry_company_wrapper.appendChild(wrapped_members_object['company']);
    industry_company_wrapper.classList.add('industry-company-wrapper');
    industry_company_wrapper.style['grid-area'] = 'industry-company-wrapper'
    reporter.appendChild(industry_company_wrapper);


    name_email_wrapper.appendChild(wrapped_members_object['name']);
    name_email_wrapper.appendChild(wrapped_members_object['email']);
    name_email_wrapper.classList.add('name-email-wrapper')
    name_email_wrapper.style['grid-area'] = 'name-email-wrapper'
    reporter.appendChild(name_email_wrapper);

    //making it expandable
    const expand_button = document.createElement('button');
    const expand_arrow = document.createElement('img');
    const expand_text = document.createElement('div');
    expand_button.classList.add('expand-button');
    expand_arrow.classList.add('expand-arrow');
    expand_text.classList.add('expand-text');

    expand_arrow.src = 'assets/Images/expand_arrow.svg';
    expand_arrow.height = 
    expand_text.innerHTML = 'Show more';

    
    expand_button.onclick = function () {
        if (!reporter.classList.contains('expanded-true')) { //collapse
            expand_text.innerHTML = 'Show less';
            expand_arrow.src = 'assets/Images/collapse_arrow.svg';
        } else {
            expand_text.innerHTML = 'Show more';
            expand_arrow.src = 'assets/Images/expand_arrow.svg';
        }
        reporter.classList.toggle('expanded-true')
        for (let member of include_when_expanded) {
            member.classList.toggle('child-expanded-true');
        }
    }

    expand_button.appendChild(expand_arrow);
    expand_button.appendChild(expand_text);

    expand_button.style['grid-area'] = "expand-button"
    reporter.appendChild(expand_button);

    //"Add button"
    const add_button = document.createElement("button");
    add_button.innerHTML = "Add";
    add_button.classList.add("add-button");
    add_button.style['grid-area'] = 'add-button';
    reporter.appendChild(add_button)

    REPORTER_WRAPPER.appendChild(wrapper);
}