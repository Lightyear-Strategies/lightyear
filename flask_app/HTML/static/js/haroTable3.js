const HARO_BODY = document.getElementById('haro-table-body')
let defaultHPP = 30;
var DATA;
let Categories = [];
const expanded_previously = {};
let mode = 'all'
let even_sibling;
const searchMenu = document.getElementById('search-menu'); 
const search_menu_ids = ['keywords','category','mediaOutlet']
let init = false;
getMediaQueryData('/api/serveHaros');



for (let id of search_menu_ids){
    document.getElementById(id).onkeydown = function(e){
        if(e.key == 'Enter'){
          document.getElementById('search-form').submit()
        }
    }
}

function submitSearch() {
    terms = {
        keywords: document.getElementById('main-search').value,
        category: document.getElementById('category-search').value,
        mediaOutlet: document.getElementById('media-outlet-search').value,
    }
    
    let requestUrl = '/api/serveHaros'
    if (mode == 'fresh') requestUrl = requestUrl + '/fresh';
    requestUrl = requestUrl + '?'

    let allEmpty = true;
    for (let e in terms){
        if (terms[e]!=''){
            allEmpty=false;
            requestUrl = `${requestUrl}${e}=${terms[e]}&`
        }
    }
    
    requestUrl = requestUrl.substring(0,requestUrl.length-1); //to remove trailing &

    if (!allEmpty){
        getMediaQueryData(requestUrl);
    } else {
        if (mode == 'all') {
            getMediaQueryData('/api/serveHaros')
        } else getMediaQueryData(`/api/serverHaros/${mode}`)
    }    
}

function getMediaQueryData(requestUrl) {
    const request = $.ajax(
      {
        'url' : requestUrl,
        success : (result, status, xhr) => {
            if (status != 304) DATA = result.data;
            page_number = 1;
            displayData();
            if (!init) {
                initializeDropdownMenus();
                init = true;
            }
        }
      }
    )
}

function insertEntry(id,datum, parent) {
    const entry = document.createElement('td');
    entry.innerHTML = datum[id];
    entry.classList.add(id);
    parent.appendChild(entry);
}

function displayData() {
    let tbodyRowCount = HARO_BODY.rows.length;
    for (let i = 0; i<tbodyRowCount; i++) HARO_BODY.deleteRow(0)

    even_sibling = false;
    for (let i = 3; i < 23; i++) {
        try {
            insertRow(DATA[i],i)
            if (even_sibling) even_sibling = false 
            else even_sibling = true
        } catch (e) {console.log(e)}
    }
    $('html,body').scrollTop(0);
}

function insertDetailsRow(id,table,datum){
    table.classList.add('details-grid');
    let label = document.createElement('div');
    let content = document.createElement('div');
    label.innerHTML = `${id}: `;
    content.innerHTML = datum[id];
    label.style['grid-area'] = `${id}-label`
    content.style['grid-area'] = id;
    label.classList.add('details-label');
    table.appendChild(label)
    table.appendChild(content)
}

function insertRow(datum,index) {
    if (datum==undefined) throw 'datum undefined';
    let row = document.createElement('tr')
    HARO_BODY.appendChild(row);
    for (let id of ['Summary','MediaOutlet','Category','DateReceived','Deadline']){
        insertEntry(id,datum,row)
    }

    const expand_button = document.createElement('button')
    expand_button.innerHTML = 'expand'
    const expand_wrapper = document.createElement('td');
    expand_wrapper.appendChild(expand_button)
    row.appendChild(expand_wrapper);
    
    row.expanded_previously = false;
    let details_wrapper
    expand_button.onclick = function() {
        //on initial expansion of a given table entry, inserts a new row containing a single cell spanning the entire column
        //the cell contians a div with class='details'. It's set to display the information as a grid
        if (!row.expanded_previously) {
            details_wrapper = HARO_BODY.insertRow(row.rowIndex);
            details_wrapper.classList.add(`even-sibling-${row.even_sibling}`)

            let details_cell = details_wrapper.insertCell();
            details_cell.colSpan = 8;
            let details = document.createElement('div');
            details_wrapper.appendChild(details_cell);
            details_cell.appendChild(details)
            for (let id of ['Journalist','Email','Query','Requirements']){
                insertDetailsRow(id,details,datum)
            }
            details.classList.add('details')
            row.expanded_previously = true;
        } else {
            details_wrapper.classList.toggle('hidden')
        }
    }

    row.classList.add(`even-sibling-${even_sibling}`)
    row.even_sibling = even_sibling
}

function initializeDropdownMenus() {
    initializeDropdownMenu(
        document.getElementById('categories'),
        'Category'
    )
    initializeDropdownMenu(
        document.getElementById('media-outlets'),
        'MediaOutlet'
    )
}

function initializeDropdownMenu(datalist,id) {
    console.log(id)
    const values = [];
    let e;
    for (let i = 0; i<15; i++){
        e = DATA[i][id]
        console.log(e)
        console.log(values.includes(e))
        if (!values.includes(e)){
            values.push(e)
        }
    }
    let option
    for (let e of values){
        
        option = document.createElement('option')
        option.value = e;
        datalist.appendChild(option);
    }
}
