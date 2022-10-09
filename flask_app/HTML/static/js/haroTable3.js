const HARO_BODY = document.getElementById('haro-table-body')
var DATA;
var FRESH_DATA;
var ALL_DATA;
let Categories = [];
const expanded_previously = {};
let mode = 'fresh'
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
let toDisplay;
let requests = [];
let request_count = 0;

let terms = {};
let terms_0 = {};
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
initializeData();
setInterval(submitSearch,100)
$( document ).ready(function() {
    //binding enter to all the search bars
    document.getElementById('dateReceived').style['background-color'] = '#F7F8FC'
    document.getElementById('dateReceived').onchange = () => {
        if (document.getElementById('date-checkbox').checked) {
            submitSearch();
        }
    }

    for (let id of search_menu_ids){ 
        document.getElementById(id).style['background-color'] = '#F7F8FC'
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
        var scroll_distance = $("#haro-table-body").scrollTop();

        if(scroll_distance > 0.9*row_height*haros_per_page*(display_index-1)) {
            if (!all_displayed) appendDisplay()
        }

        updateHaroCounter()
    });

})

function checkSearch() {
    console.log('check search')
    
}

function getDates() {
    strDates = document.getElementById('dateReceived').value

    let  from  = strDates.substring(0,10)
    let to = strDates.substring(13)
    return [from + ' 00:00:00', to + ' 23:59:59']
}

function submitSearch(newmode = false) {
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

    if (JSON.stringify(terms).length == 2) {
        if (mode == 'fresh') DATA = FRESH_DATA;
        else DATA = ALL_DATA;
        return;
    }

    if (!newmode) {
        if ((JSON.stringify(terms) == JSON.stringify(terms_0))) return;
    }

    terms_0 = terms;

    let requestUrl = '?'

    for (let e in terms){
        if (terms[e]!=''){
            requestUrl = `${requestUrl}${e}=${terms[e]}&`
        }
    }
    
    requestUrl = requestUrl.substring(0,requestUrl.length-1); //to remove trailing & or make string empty

    if (mode == 'fresh') getMediaQueryData('/api/serveHaros/fresh' + requestUrl)
    else getMediaQueryData('api/serveHaros' + requestUrl)

}

function initializeData() {
    $.ajax(
        {
            'url' : '/api/serveHaros/fresh',
            success : (result, status, xhr) => {
                if (status != 304) {
                    FRESH_DATA = result.data;
                    DATA = FRESH_DATA;
                }
                page_number = 1;
                resetDisplay();
                appendDisplay();
                initializeDropdownMenus();
                init = true;
            }
        }
    )

    $.ajax(
        {
            'url' : '/api/serveHaros',
            success : (result, status, xhr) => {
                if (status != 304) {
                    ALL_DATA = result.data;
                }
            }
        }
    )

}

function getMediaQueryData(requestUrl) {
    request_count = request_count + 1;
    const request_no = request_count;

    const request = $.ajax(
      {
        'url' : requestUrl,
        success : (result, status, xhr) => {
            if (status != 304) DATA = result.data;
            page_number = 1;
            if (request_no == request_count) {
                resetDisplay();
                appendDisplay();
                if (!init) {
                    initializeDropdownMenus();
                    init = true;
                }
            }
        }
      }
    )
    requests.push(request)
}

function updateHaroCounter() {
    const htb = document.getElementById('haro-table-body')
    const row_height = (htb.childNodes)[0].offsetHeight;
    var scroll_distance = $("#haro-table-body").scrollTop();
    const len = toDisplay.length;
    if (len <= 6) {
        document.getElementById('haro-counter').innerHTML = `${len} / ${len} Requests viewed`
    } else {
        document.getElementById('haro-counter').innerHTML = `${Math.floor((scroll_distance)/row_height+htb.offsetHeight/row_height+.9)} / ${len} Requests viewed`
    }

}

function resetDisplay() {
    all_displayed = false;
    display_index = 0;
    $('#haro-table-body > *').remove()
    
    document.getElementById('table-head').classList.remove('hidden')
    document.getElementById('haro-table-body').classList.remove('underflown')
}

function appendDisplay() {

    toDisplay = [];
    if (mode == 'saved') {
        for (let e of DATA) {
            if (saved_haros_indicies.has(e.index)) toDisplay.push(e)
        }
    } else toDisplay = DATA
    let summaries = [];
    for (let e of toDisplay) {
        summaries.push(e['Summary'])
    }
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
    updateHaroCounter()
    lastUpdated()

}



function insertDetailsRow(id, table, datum) {
     
    table.classList.add('details-grid');
    let label = document.createElement('div');
    let content;
    if (id == 'Email') {
        let email;
        let btnCopy;
        let tooltip;

        content = document.createElement('span');

        email = document.createElement('a');
        email.href = 'mailto:' + datum[id];
        email.innerHTML = datum[id];

        btnCopy = document.createElement('a');
        btnCopy.onclick = copyEmailToClipboard(datum[id]);
        btnCopy.classList.add('copyButton');

        tooltip = document.createElement('span');
        tooltip.innerText = "Copy to clipboard";
        tooltip.classList.add('tooltip-txt');


        content.appendChild(email);
        content.appendChild(btnCopy);
        content.appendChild(tooltip);

    }
    else {
        content = document.createElement('div');

        if (id=='Journalist'){
            content.innerHTML = datum['Name']
        }
        else {
            content.innerHTML = datum[id];
        }
    }
    label.innerHTML = `${id}: `;
    label.style['grid-area'] = `${id}-label`
    content.style['grid-area'] = id;
    label.classList.add('details-label');
    table.appendChild(label)
    table.appendChild(content)
}


async function copyEmailToClipboard(copy) {
    try {
        await navigator.clipboard.writeText(copy);
    }
    catch (err) {
        console.log(err)
    }
  
  
}


function insertEntry(id,datum, parent) {
    
    const entry = document.createElement('div');
    if (id == 'DateReceived') {
        entry.innerHTML = datum['DateReceived'].substring(5,7) + '/' + datum['DateReceived'].substring(8) + '/' + datum['DateReceived'].substring(0,4);
    } else if (id == 'Deadline') {
        try {
            deadlineArr = datum['Deadline'].split(' ');
            let dlday = deadlineArr[4];
            if (dlday.length == 1) dlday = '0' + dlday;
            entry.innerHTML = monthToNum(deadlineArr[5]) + '/' + dlday + ' ' + (deadlineArr[0].split(':'))[0] + deadlineArr[1];
        }
        catch (err) {
            // catches poorly formatted due dates and throws them away
            entry.innerHTML = '';
        }
    } else {
        entry.innerHTML = datum[id];
    }

    entry.classList.add(id);
    entry.style['grid-area'] = id
    entry.style['align-self'] = 'center'
    parent.appendChild(entry);
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
            details.onclick = function(e) {
                e.stopPropagation();
            }
            row.classList.add('expanded')
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
        

        if(!row.saved && mode == 'saved') {
            $( row ).remove()
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
    document.getElementById('table-head').classList.add('hidden')
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
        HARO_BODY.classList.remove(mode);
        HARO_BODY.classList.add(btnmode);
        document.getElementById(mode + '-btn').classList.remove('selected');
        document.getElementById(btnmode + '-btn').classList.add('selected');
        mode = btnmode
        submitSearch(true);
        resetDisplay();
        appendDisplay();
    }
}



function saveSavedHaros() {
    istr = ''
    for (let i of saved_haros_indicies) {
        istr = `${istr} ${i}`
    }
    localStorage.setItem('saved_haros_indicies',istr)
}

function getSavedHaros() {
    let strArray
    try {
        strArray = (localStorage.getItem('saved_haros_indicies')).split(' ')
    } catch (e) {
        strArray = [];
    }
    
    for (let istr of strArray) {
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


// //Load screen? Idk
// let toastAppear = false;
// const toast = (type, text) => {
//     if (toastAppear == true) return;

//     const toast = document.querySelector(".toast");
//     const toastLoader = document.querySelector(".toast-loader");
//     const toastText = document.querySelector(".toast-content > h2");

//     toast.style.visibility = "visible";
//     toastLoader.style.visibility = "visible";
//     toastText.innerHTML = text;
//     toastLoader.style.transition = "linear width 1.2s";
//     toastAppear = true;

//     if (type == "error") 
//         toastLoader.style.backgroundColor = "var(--lightyear-red)";
//     else if (type == "info") 
//         toastLoader.style.backgroundColor = "var(--lightyear-blue)";
//     else
//         toastLoader.style.backgroundColor = "var(--lightyear-yellow)"

//     setTimeout(() => {
//         toastLoader.classList.add("toast-loader-end");
//     }, 200);

//     setTimeout(() => {
//         toast.style.visibility = "hidden";
//         toastLoader.style.visibility = "hidden";
//         toastLoader.style.transition = "none";
//         toastLoader.classList.remove("toast-loader-end")
//         toastAppear = false;
//     }, 1500);
// }

// function endLoad() {
//     document.querySelector(".toast").style.visibility = "hidden";
//     document.querySelector(".toast-loader").style.visibility = "hidden";
//     load();
// }

// function load() {
//     let loader = document.querySelector("#loader"); 
//     setTimeout(() => {
//         loader.style.transform = "translateY(-100%)"; 
//     }, 1500);
// }

function isOverflown(element) {
    return element.scrollHeight > element.clientHeight
  }


  // Establish when the Haro Table was last updated 

function time_ago(time) {

  switch (typeof time) {
    case 'number':
      break;
    case 'string':
      time = +new Date(time);
      break;
    case 'object':
      if (time.constructor === Date) time = time.getTime();
      break;
    default:
      time = +new Date();
  }
  var time_formats = [
    [60, 'seconds', 1], // 60
    [120, '1 minute ago', '1 minute from now'], // 60*2
    [3600, 'minutes', 60], // 60*60, 60
    [7200, '1 hour ago', '1 hour from now'], // 60*60*2
    [86400, 'hours', 3600], // 60*60*24, 60*60
    [172800, 'Yesterday', 'Tomorrow'], // 60*60*24*2
    [604800, 'days', 86400], // 60*60*24*7, 60*60*24
    [1209600, 'Last week', 'Next week'], // 60*60*24*7*4*2
    [2419200, 'weeks', 604800], // 60*60*24*7*4, 60*60*24*7
    [4838400, 'Last month', 'Next month'], // 60*60*24*7*4*2
    [29030400, 'months', 2419200], // 60*60*24*7*4*12, 60*60*24*7*4
    [58060800, 'Last year', 'Next year'], // 60*60*24*7*4*12*2
    [2903040000, 'years', 29030400], // 60*60*24*7*4*12*100, 60*60*24*7*4*12
    [5806080000, 'Last century', 'Next century'], // 60*60*24*7*4*12*100*2
    [58060800000, 'centuries', 2903040000] // 60*60*24*7*4*12*100*20, 60*60*24*7*4*12*100
  ];
  var seconds = (+new Date() - time) / 1000,
    token = 'ago',
    list_choice = 1;

  if (seconds == 0) {
    return 'Just now'
  }
  if (seconds < 0) {
    seconds = Math.abs(seconds);
    token = 'from now';
    list_choice = 2;
  }
  var i = 0,
    format;
  while (format = time_formats[i++])
    if (seconds < format[0]) {
      if (typeof format[2] == 'string')
        return format[list_choice];
      else
        return Math.floor(seconds / format[2]) + ' ' + format[1] + ' ' + token;
    }
  return time;
}


function lastUpdated() {
    let lastUpdate = document.getElementById("getDateUpdate").innerText;
    let update=time_ago(lastUpdate);
    document.getElementById("last-updated").innerHTML = "Last updated "+update;
}

//refresh last updated every 5 minutes
setInterval(function(){ 
    lastUpdated()    
}, 300000);

