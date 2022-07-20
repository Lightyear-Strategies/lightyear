const HAROS_TABLE = document.getElementById("haros-table");
let defaultHPP = 30;
let DATA;
let Categories = [];
const expanded_previously = {};
let mode = 'all'

initializeHarosPerPAge();
getMediaQueryData('/api/serveHaros');

function initializeHarosPerPAge(){
    
    haros_per_page = Number(localStorage.getItem('harosPerPage'));
    
    if (haros_per_page == undefined || haros_per_page == 0){
        console.log('if')
        haros_per_page = 30;
    }
    document.getElementById('item-count-input').value = haros_per_page
    console.log(haros_per_page);
}

function applyHarosCount() {
    console.log('applyHarosCount');
    haros_per_page = document.getElementById('item-count-input').value
    localStorage.setItem('haros_per_page',haros_per_page);
    page_number = 1;
    displayData();
}

function getMediaQueryData(requestUrl) {
    
    const request = $.ajax(
      {
        'url' : requestUrl,
        success : (result, status, xhr) => {

            DATA = result.data;
            page_number = 1;
            //configDropdownMenus();8
            displayData();
        }

      }
    )
}


document.getElementById('all-haros').onclick = () => {
    mode = 'all'
  page_number = 0;
  getMediaQueryData('/api/serveHaros')
}

document.getElementById('fresh-haros').onclick = () => {
    mode = 'fresh'
  page_number = 0;
  getMediaQueryData('/api/serveHaros/fresh')
}

document.getElementById('used-haros').onclick = () => {
    mode = 'used'
  page_number = 0;
  getMediaQueryData('/api/serveHaros/used')
}

function displayData() {
    console.log(`hpp ${haros_per_page} pn ${page_number} Data length ${DATA.length}`)
    $('.haros-table *').remove();
    console.log
    let min_index = haros_per_page*(page_number-1);

    let max_index = haros_per_page*page_number;
    if (max_index > DATA.length) max_index = DATA.length;
    console.log([min_index,max_index])
    for (let i = min_index; (i < max_index); i++) {
        try {
        insert_datum(DATA[i]);
        } catch (error) {
            console.log('error')
        }
    }
    $('html,body').scrollTop(0);
}

function next_page() {
    if (page_number*haros_per_page<DATA.length){
        page_number = page_number + 1;
        displayData();
    }

}

function previous_page() {
    if (page_number > 1){
        page_number = page_number - 1;
        displayData();
    }
}

function std_make(class_name, parent, ops) { //optional parameters: ops.content, ops.tag
    if (ops == undefined ) ops = {
        content: '',
        tag: 'div',
    }
    if (ops.content == undefined ) ops.content = "";
    if (ops.tag == undefined ) ops.tag = 'div'

    const doc_element = document.createElement(ops.tag);
    doc_element.classList.add(class_name);
    doc_element.innerHTML = ops.content;
    parent.appendChild(doc_element);

    return doc_element
}

function insert_datum(d) {
    
    const datum_grid = std_make('datum-grid',HAROS_TABLE, {grid_child: false})
    datum_grid.classList.add('hide');
    datum_grid.expanded_previously = false;
    datum_grid.expanded = false;
    const include_when_expanded = [];

    const header = std_make('header',datum_grid);
    


    const expand_button = std_make('expand-button',header, {tag: 'button'});
    expand_button.innerHTML = 'v';
    const summary_mediaOutlet_wrapper = std_make('summary_mediaOutlet_wrapper',header)
    //data to display
    const summary = std_make('Summary',summary_mediaOutlet_wrapper,{content: d['Summary']})
    const mediaOutlet = std_make('MediaOutlet',summary_mediaOutlet_wrapper,{content:d['MediaOutlet']})

    const dateReceived = std_make('DateReceived',header,{
        content:dateConvert(d['DateReceived'])
    })

    datum_grid.onclick = function () {
        if (!datum_grid.expanded_previously) {

            const name_email_wrapper = std_make('name-email-wrapper', datum_grid );
            const name_email_header = std_make('name-email-header',name_email_wrapper,{content:"Contact: ", tag: 'span'})
            const name = std_make('Name',name_email_wrapper,{content: d['Name'], tag: 'span'})
            const email = std_make('Email',name_email_wrapper,{content: d['Email'], tag: 'span'})
            
            const category = std_make('Category',datum_grid,{content:`Category: ${d['Category']}`})
            
            const deadline = std_make('Deadline',datum_grid,{
                content:("Deadline: "+ d['Deadline']), tag: 'span'
            })

            const query_wrapper = std_make('query-wrapper',datum_grid);
            const query_header = std_make('query-header',query_wrapper, {content:"Query: "})
            const query = std_make('Query',query_wrapper, {content:d['Query'], grid_child: false})

            const requirements_wrapper = std_make('requirements-wrapper',datum_grid);
            const requirements_header = std_make('requirements-header',requirements_wrapper, {content:"Requirements: "})
            const requirements = std_make('Requirements',requirements_wrapper,{content: d['Requirements']})
            /*function () {

                for (let member of include_when_expanded){
                    member.classList.toggle('hide')
                }
            } */

            include_when_expanded.push(name_email_wrapper);
            include_when_expanded.push(query_wrapper);
            include_when_expanded.push(requirements_wrapper);
            include_when_expanded.push(deadline);
            include_when_expanded.push(category);

            datum_grid.expanded_previously = true;
            for (let member of include_when_expanded) {
                member.classList.toggle('hide')
            }
        }
        if(datum_grid.expanded) {
          expand_button.innerHTML = 'v'
          datum_grid.expanded = false;
        } else {
          expand_button.innerHTML = '^'
          datum_grid.expanded = true;
        }
            
        for (let member of include_when_expanded) {
            member.classList.toggle('hide');
        }
    }

    //Additional collapse button
    


    //"Add button"
    let str;
    if (d['Used']=='Used') 
    {
        str = 'Remove'
        datum_grid.classList.add('used-true');
    }
    else str = 'Add'
    const add_button = std_make(
        'add-button',
        header,
        {
            content: str, 
            tag:'button',
            grid_child: true
        }
    )

    add_button.onclick = function(e) {
        if (this.innerHTML == "Add") {
            this.innerHTML = "Remove"
            $.ajax("/api/used/add/"+d['index'])
        } else {
            this.innerHTML = "Add"
            $.ajax("/api/used/remove/"+d['index'])
        }
        datum_grid.classList.toggle('used-true')
        e.stopPropagation();
    }
    
    

    datum_grid.classList.remove('hide');
}


document.getElementById('search-button').onclick = () => {
    terms = {
        keywords: document.getElementById('keywords-search').value,
        journalist: document.getElementById('journalist-search').value,
        mediaOutlet: document.getElementById('mediaOutlet-search').value,
        dateBefore: document.getElementById('dateBefore-search').value,
        dateAfter: document.getElementById('dateAfter-search').value
        }
    for (let e of ['dateBefore','dateAfter']){
        terms[e] = terms[e].substring(5,7)+'/'+terms[e].substring(8,10)+'/'+terms[e].substring(0,4)
    }
    terms['dateBefore'] = terms['dateBefore'] + ' 23:59:59'
    terms['dateAfter'] = terms['dateAfter'] + ' 00:00:00'
    let requestUrl = '/api/serveHaros'
    if (mode == 'fresh') requestUrl = requestUrl + '/fresh';
    if (mode == 'used') requestUrl = requestUrl + '/used';
    requestUrl = requestUrl + '?'

    let allEmpty = true;
    for (let e in terms){
        if (terms[e]!=''){
            console.log(terms[e])
            allEmpty=false;
            requestUrl = `${requestUrl}${e}=${terms[e]}&`
        }
    }
    console.log(requestUrl)
    requestUrl = requestUrl.substring(0,requestUrl.length-1);
    if (!allEmpty){
        getMediaQueryData(requestUrl);
    } else {
        if (mode == 'all') {
            getMediaQueryData('/api/serveHaros')
        } else getMediaQueryData(`/api/serverHaros/${mode}`)
    }    
}


function dateConvert(date){
    // yyyy-mm-dd to dd (month), yyyy
    months = [undefined, 'Jan','Fed','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    return months[Number(date.substring(5,7))] + ' ' + date.substring(8) + ', ' + date.substring(0,4);
}