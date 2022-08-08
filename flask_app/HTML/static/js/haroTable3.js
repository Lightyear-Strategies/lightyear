const HARO_BODY = document.getElementById('haro-table-body')
let defaultHPP = 30;
var DATA;
let Categories = [];
const expanded_previously = {};
let mode = 'all'
const searchMenu = document.getElementById('search-menu'); 
const search_menu_ids = ['keywords','category','mediaOutlet']
let init = false;
let page = 1;
let display_index = 0;
const search_bar_toggle_elements = [
    document.getElementById('filter-btn'),
    document.getElementById('mediaOutlet-label'),
    document.getElementById('mediaOutlet'),
    document.getElementById('category-label'),
    document.getElementById('category'),
    document.getElementById('search-collapse-button'),
    document.getElementById('dateReceived-label'),
    document.getElementById('dateReceived'),
    document.getElementById('date-checkbox')
]
let haros_per_page = 100;
let saved_iterator;
let all_displayed;


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


initializeGridAreas(
    document.getElementById('search-menu')
)
saved_haros_indicies = new Set()
getSavedHaros()
getMediaQueryData('/api/serveHaros');


$( document ).ready(function() {
    //binding enter to all the search bars
    document.getElementById('dateReceived').style['background-color'] = '#F7F8FC'
    for (let id of search_menu_ids){
        e = document.getElementById(id)
        e.style['background-color'] = '#F7F8FC'
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
    
    $("#haro-table-body").scroll(function() {
        const htb = document.getElementById('haro-table-body')
        const row_height = (htb.childNodes)[0].offsetHeight;
        
        //console.log(`element height?: ${[0].height()*haros_per_page}`
        if($("#haro-table-body").scrollTop() > 0.9*row_height*haros_per_page*(display_index-1)) {
            if (!all_displayed) appendDisplay()
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
            resetDisplay();
            appendDisplay();
            if (!init) {
                initializeDropdownMenus();
                init = true;
            }
        }
      }
    )
}



function resetDisplay() {
    all_displayed = false;
    display_index = 0;
    $('#haro-table-body > *').remove()
    

    document.getElementById('haro-table-body').classList.remove('underflown')
}

function appendDisplay() {

    let toDisplay = [];
    if (mode == 'saved') {
        for (let e of DATA) {
            if (saved_haros_indicies.has(e.index)) toDisplay.push(e)
        }
    } else toDisplay = DATA
    console.log(toDisplay)
    if (toDisplay.length == 0) {
        noHarosDisplay();
    }

    let len = toDisplay.length

    let min_index = haros_per_page * display_index;
    let max_index = min_index + haros_per_page;
    display_index = display_index + 1;

    let iterations = 0;
    for (let i = min_index; i < max_index; i++) {
        try {
            if (i >= len) {
                all_displayed = true;
                if (!isOverflown(document.getElementById('haro-table-body'))){
                    document.getElementById('haro-table-body').classList.add('underflown')
                }
                break;
            }
            if (iterations > 2000) break
            iterations = iterations + 1;
            insertRow(toDisplay[i])

        } catch (e) {
            i = i - 1; 
            console.log(e); 
        }
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

function insertEntry(id,datum, parent) {
    
    const entry = document.createElement('div');
    if (id == 'DateReceived') {
        entry.innerHTML = datum['DateReceived'].substring(5,7) + '/' + datum['DateReceived'].substring(8) + '/' + datum['DateReceived'].substring(0,4);
    } else if (id == 'Deadline') {
        deadlineArr = datum['Deadline'].split(' ');

        let dlday = deadlineArr[4];
        if (dlday.length == 1) dlday = '0' + dlday;
        entry.innerHTML = monthToNum(deadlineArr[5]) + '/' + dlday + ' ' + (deadlineArr[0].split(':'))[0] + deadlineArr[1];
    } else {
        entry.innerHTML = datum[id];
    }

    entry.classList.add(id);
    entry.style['grid-area'] = id
    entry.style['align-self'] = 'center'
    parent.appendChild(entry);
}

function insertRow(datum) {
    if (datum.Summary == '"Rotten Egg" Flatulence' || datum.Summary == 'Garlic Breath') return
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
    row.onclick = function() {
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

    //insert bookmark button
    let save_button = document.createElement('button')
    save_button.style['grid-area'] = 'save-button'
    save_button.classList.add('save-button')
    if(datum.index == 0) {
        console.log(saved_haros_indicies)
    }
    if (saved_haros_indicies.has(datum.index)) {
        row.saved = true;
        save_button.classList.add('saved')
    } else {
        row.saved = false;
    }

    save_button.onclick = (e) => { 
        if (row.saved) {
            row.saved = false;
            saved_haros_indicies.delete(Number(datum.index))
        } else {
            row.saved = true;
            saved_haros_indicies.add(Number(datum.index))
        }
        save_button.classList.toggle('saved')

        e.stopPropagation();
    }
    row.onmouseleave = () => {
        
        console.log('mouseout')
        if(!row.saved && mode == 'saved') {
            $( row ).remove()
            console.log(document.getElementById('haro-table-body').childNodes.length)
            if (document.getElementById('haro-table-body').childNodes.length == 0) {
                noHarosDisplay();
            }
        }
        
    }
    row.appendChild(save_button);
}

function noHarosDisplay() {
    let err = document.createElement('div')
    err.classList.add('none-to-display-error')
    if (mode == 'saved') {
        err.innerHTML = 'No saved queries at this time :)'
    } else {
        err.innerHTML = 'Sorry! No Haros match your query :('
    }
    document.getElementById('haro-table-body').appendChild(err)
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

    if (btnmode != mode) {
        mode = btnmode
        document.getElementById('haro-table-body').classList.toggle('saved')
        resetDisplay();
        appendDisplay();
        for (let e of document.getElementsByClassName('search-tab')) {
            e.classList.toggle('selected')
        }
    }
    console.log(mode)
}



function saveSavedHaros() {
    istr = ''
    for (let i of saved_haros_indicies) {
        istr = `${istr} ${i}`
    }
    localStorage.setItem('saved_haros_indicies',istr)
}

function getSavedHaros() {

    const strArray = localStorage.getItem('saved_haros_indicies').split(' ')
    console.log(strArray)
    for (let istr of strArray) {
        console.log(istr)
        if (istr != '') {
            saved_haros_indicies.add(Number(istr))
        }

    }

}

function monthToNum(str) {
    let num = ['01','02','03','04','05','06','07','08','09','10','11','12'];
    let month = ['January','Feburary','March','April','May','June','July','August','September','October','November','December']
    return num[month.indexOf(str)]
}

function logSaved() {
    console.log(saved_haros_indicies)
}

//Load screen? Idk
let toastAppear = false;
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

window.onload = () => {
    document.querySelector(".toast").style.visibility = "hidden";
    document.querySelector(".toast-loader").style.visibility = "hidden";
    document.querySelector("body").style.overflowY = "hidden";
    load();
}

const load = () => {
    let loader = document.querySelector("#loader"); 
    setTimeout(() => {
        loader.style.transform = "translateY(-100%)"; 
        document.querySelector("body").style.overflowY = "inherit";
    }, 1500);
}

function isOverflown(element) {
    return element.scrollHeight > element.clientHeight
  }