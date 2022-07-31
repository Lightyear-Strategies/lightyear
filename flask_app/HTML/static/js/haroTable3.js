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
let page = 1;
const search_bar_toggle_elements = [
    document.getElementById('filter-btn'),
    document.getElementById('mediaOutlet-label'),
    document.getElementById('media-outlet-wrapper'),
    document.getElementById('category-label'),
    document.getElementById('category'),
    document.getElementById('search-collapse-button'),
    document.getElementById('dateReceived-label'),
    document.getElementById('dateReceived'),
    document.getElementById('date-checkbox')
]
let haros_per_page = 100;
let saved_iterator;


/*
if (localStorage.getItem('saved_haros_indicies') == undefined) saved_haros_indicies = new Set() 
else saved_haros_indicies = localStorage.getItem('saved_haros_indicies')
*/

//gotta do it like this because idk how to configure browser files
const rightArrowSvg = `<svg width="9" height="13" viewBox="0 0 9 13" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M0.996094 12L7.99609 6.5L0.996094 1" stroke="#252733" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
`
const leftArrowSvg =`<svg width="9" height="13" viewBox="0 0 9 13" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M8 1L1 6.5L8 12" stroke="#888A96" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
`
const downArrowSvg =`
<svg width="13" height="9" viewBox="0 0 13 9" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M1.12634 1L6.61271 8L12.0991 1" stroke="#252733" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
`

const noSaveSvg =`
<svg width="14" height="16" viewBox="0 0 14 16" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12.5237 14.75L7.02305 11.9375L1.52368 14.75V2.375C1.52368 2.22582 1.59611 2.08274 1.72505 1.97725C1.85398 1.87176 2.02885 1.8125 2.21118 1.8125H11.8362C12.0185 1.8125 12.1934 1.87176 12.3223 1.97725C12.4512 2.08274 12.5237 2.22582 12.5237 2.375V14.75Z" stroke="#A4A6B3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
`

const saveHoverSvg =`
<svg width="14" height="16" viewBox="0 0 14 16" fill="#A4A6B3" xmlns="http://www.w3.org/2000/svg">
<path d="M12.5237 14.75L7.02305 11.9375L1.52368 14.75V2.375C1.52368 2.22582 1.59611 2.08274 1.72505 1.97725C1.85398 1.87176 2.02885 1.8125 2.21118 1.8125H11.8362C12.0185 1.8125 12.1934 1.87176 12.3223 1.97725C12.4512 2.08274 12.5237 2.22582 12.5237 2.375V14.75Z" stroke="#A4A6B3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
`

const saveSvg =`
<svg width="14" height="16" viewBox="0 0 14 16" fill="black" xmlns="http://www.w3.org/2000/svg">
<path d="M12.5237 14.75L7.02305 11.9375L1.52368 14.75V2.375C1.52368 2.22582 1.59611 2.08274 1.72505 1.97725C1.85398 1.87176 2.02885 1.8125 2.21118 1.8125H11.8362C12.0185 1.8125 12.1934 1.87176 12.3223 1.97725C12.4512 2.08274 12.5237 2.22582 12.5237 2.375V14.75Z" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
`


initializeGridAreas(
    document.getElementById('search-menu')
)
getMediaQueryData('/api/serveHaros');


$( document ).ready(function() {
    //binding enter to all the search bars
    for (let id of search_menu_ids){
        e = document.getElementById(id)

        e.onkeydown = function(e){

            if(e.key == 'Enter'){

                submitSearch()
            }
        }
    }


    $('input[name="dateReceived"]').daterangepicker({
        timePicker: false,
        startDate: moment().startOf('hour'),
        endDate: moment().startOf('hour').add(32, 'hour'),
        locale: {
          format: 'MM/DD/YYYY'
        }
      });
})


function getDates() {
    strDates = document.getElementById('dateReceived').value

    let  from  = strDates.substring(0,10)
    let to = strDates.substring(13)
    return [from + ' 00:00:00', to + ' 23:59:59']
}

function submitSearch() {
    dateRange = getDates()
    terms = {
        keywords: document.getElementById('keywords').value,
        category: document.getElementById('category').value,
        mediaOutlet: document.getElementById('mediaOutlet').value,
        dateAfter: '',
        dateBefore: '',
    }
    if (document.getElementById('date-checkbox').checked) {
        terms.dateAfter = dateRange[0];
        terms.dateBefore = dateRange[1];
    }

    let requestUrl = '/api/serveHaros'
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
        getMediaQueryData('/api/serveHaros')
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
    const entry = document.createElement('div');
    entry.innerHTML = datum[id];
    entry.classList.add(id);
    entry.style['grid-area'] = id
    parent.appendChild(entry);
}

function pageNav(direction) {
    let length = DATA.length
    if (direction == 'next' && haros_per_page*page < length ) page = page + 1
    if (direction == 'previous' && page > 1) page = page - 1;
    displayData()
}

function displayData() {
    console.log('displayData()')
    toDisplay = [];
    if (mode == 'saved') {
        for (let e of DATA) {
            if (saved_haros_indicies.has(DATA.index)) toDisplay.push(e)
        }
    } else toDisplay = DATA
    $('#haro-table-body > *').remove()
    console.log(toDisplay)
    even_sibling = false;
    let min_index = haros_per_page*(page-1);
    let max_index = haros_per_page*page;
    if (max_index > toDisplay.length) max_index = toDisplay.length;

    if (max_index > toDisplay.length) max_index = toDisplay.length;
    let iterations = 0;
    for (let i = min_index; i < max_index ; i++) {
        try {
            if (iterations > 2000) break
            iterations = iterations + 1;
            insertRow(toDisplay[i])
            if (even_sibling) even_sibling = false 
            else even_sibling = true
        } catch (e) {i = i - 1}
    }
    $('html,body').scrollTop(0);
    
    if (document.getElementById('bottom-nav').classList.contains('hidden')) {
        document.getElementById('bottom-nav').classList.remove('hidden')
    }
}

function insertDetailsRow(id,table,datum){
    table.classList.add('details-grid');
    let label = document.createElement('div');
    let content = document.createElement('div');
    label.innerHTML = `${id}: `;
    
    label.style['grid-area'] = `${id}-label`
    content.style['grid-area'] = id;
    label.classList.add('details-label');
    table.appendChild(label)
    table.appendChild(content)
    if (id=='Journalist'){
        content.innerHTML = datum['Name']
    } else {
        content.innerHTML = datum[id];
    }
}

function insertRow(datum) {
    if (datum==undefined) throw 'datum undefined';
    let row = document.createElement('div')
    row.classList.add('haro-row')
    HARO_BODY.appendChild(row);
    for (let id of ['Summary','MediaOutlet','Category','DateReceived','Deadline']){
        insertEntry(id,datum,row)
    }

    const expand_button = document.createElement('button')
    expand_button.innerHTML = rightArrowSvg
    expand_button.style['grid-area'] = 'expand-button'
    row.appendChild(expand_button)


    row.expanded_previously = false;
    row.expanded = false;
    let details
    expand_button.onclick = function() {
        //on initial expansion of a given table entry, inserts a new row containing a single cell spanning the entire column
        //the cell contians a div with class='details'. It's set to display the information as a grid
        if (!row.expanded_previously) {
            details = document.createElement('div');
            row.appendChild(details)
            for (let id of ['Journalist','Email','Query','Requirements']){
                insertDetailsRow(id,details,datum)
            }
            details.classList.add('details')
            row.expanded_previously = true;
        } else {
            details.classList.toggle('hidden')
            row.classList.toggle('expanded')  
        }
        if (row.expanded) {
            row.expanded = false;
            expand_button.innerHTML = rightArrowSvg
        } else {
            row.expanded = true
            expand_button.innerHTML = downArrowSvg
        }
    }

    //for coloring backgrounds
    row.classList.add(`even-sibling-${even_sibling}`)
    row.even_sibling = even_sibling

    //insert bookmark button
    save_button = document.createElement('button')
    save_button.style['grid-area'] = 'save-button'
    save_button.innerHTML = noSaveSvg;
    row.appendChild(save_button)
    if (saved_haros_indicies.has(datum.index)) row.saved = true;
    else row.saved = false;
    save_button.onclick = replaceSaveButton(row,datum)
}

function replaceSaveButton(parent,datum,oldSaveButton){
    let flag = false;
    if (oldSaveButton) {
        oldSaveButton.remove()
        flag = true;
    }
    let save_button = document.createElement('button')
    save_button.style['grid-area'] = 'save-button'
    if (parent.saved) save_button.innerHTML = saveSvg
    else save_button.innerHTML = noSaveSvg
    parent.appendChild(save_button)
    save_button.onclick = function() {
        if (parent.saved) {
            saved_haros_indicies.delete(Number(datum.index))
            parent.saved = false
        } else {
            saved_haros_indicies.add(Number(datum.index))
            parent.saved = true
        }
        replaceSaveButton(parent,datum,save_button)
    }
    
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

    const values = [];
    let e;
    for (let i = 0; i<DATA.length; i++){
        e = DATA[i][id]

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

function toggleExpandedSearchBar(){
    document.getElementById('search-menu').classList.toggle('expanded')
    for (let e of search_bar_toggle_elements) {
        e.classList.toggle('hidden')
    }
}

function initializeGridAreas(grid){

    let children = grid.childNodes

    for (let node of children) {

        if (node.tagName == 'INPUT' || node.tagName == 'DIV' || node.tagName == 'BUTTON') {
            node.style['grid-area'] = node.getAttribute('id')
        }
    }
}

function toggleDatePicker() {
    for (let id of ['dateReceived-label','dateReceived']) {
        document.getElementById(id).classList.toggle('disabled')
    }
}

function switchTable(btnmode) {
    console.log(saved_haros_indicies)
    if (btnmode != mode) {
        mode = btnmode
        displayData();
        for (let e of document.getElementsByClassName('search-tab')) {
            e.classList.toggle('selected')
        }
    }
}

saved_haros_indicies = new Set()
getSavedHaros()

function saveSavedHaros() {
    localStorage.setItem('test','true')
    istr = ''
    for (let i of saved_haros_indicies) {
        istr = `${istr} ${i}`
    }
    localStorage.setItem('saved_haros_indicies',istr)
}

function getSavedHaros() {
    const strArray = localStorage.getItem('saved_haros_indicies').split(' ')
    for (let istr of strArray) {
        saved_haros_indicies.add(Number(istr))
    }

}



function logSaved() {
    console.log(saved_haros_indicies)
}