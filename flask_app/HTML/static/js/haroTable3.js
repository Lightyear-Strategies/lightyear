const HARO_BODY = document.getElementById('haro-table-body')
let defaultHPP = 30;
let DATA;
let Categories = [];
const expanded_previously = {};
let mode = 'all'

getMediaQueryData('/api/serveHaros');


function getMediaQueryData(requestUrl) {
    const request = $.ajax(
      {
        'url' : requestUrl,
        success : (result, status, xhr) => {
            if (status != 304) DATA = result.data;
            page_number = 1;
            displayData();
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
    let row;
    let datum;
    let savebtn;
    let saveimg;

    for (let i = 0; i < 20; i++) {
        datum = DATA[i]
        row = document.createElement('tr')
        HARO_BODY.appendChild(row);

        for (let id of ['Summary','MediaOutlet','Category','DateReceived','Deadline']){
            insertEntry(id,datum,row)
        }
    }
}