document.getElementById('all-haros').onclick = () => {
    console.log('serving normal')
    page_number = 0;
    getMediaQueryData('/api/serveHaros')
  }
  
  document.getElementById('fresh-haros').onclick = () => {
    console.log('serving fresh')
    page_number = 0;
    getMediaQueryData('/api/serveHaros/fresh')
  }
  
  document.getElementById('used-haros').onclick = () => {
    console.log('serving used')
    page_number = 0;
    getMediaQueryData('/api/serveHaros/used')
  }
  
  const HAROS_TABLE = document.getElementById("haros-table");
  
  let DATA;
  let Categories = [];
  let page_number = 0;
  let haros_per_page = document.getElementById('haros-per-page').value;
  const expanded_previously = {};
  
  document.getElementById('haros-per-page').onfocusout = () => {
      ohpp = haros_per_page //old haros per page
      opn = page_number //old page number
      if (this.value < 10) {
          this.value = 10;
      }
      if (this.value > 1000) {
          this.value = 1000;
      }
      haros_per_page = this.value;
      page_number = Math.floor((opn*ohpp+1)/haros_per_page);
      displayData();
  }
  
  getMediaQueryData('/api/serveHaros');
  
  function getMediaQueryData(requestUrl) {
      
      const request = $.ajax(
        {
          'url' : requestUrl,
          success : (result, status, xhr) => {
            DATA = result.data;
            const e = document.createElement('div')
            console.log(DATA);
            displayData();
            //configDropdownMenus();
          }
  
        }
      )
  }
  
  function displayData() {
      $('.haros-table *').remove();
      const min_index = haros_per_page*(page_number-1);
      
      const max_index = Math.min([
          haros_per_page*page_number,
          DATA.length
      ])
  
      for (let i = min_index; (i < max_index && i< DATA.length); i++) {
          try {
          insert_datum(DATA[i]);
          } catch (error) {
              console.log('error')
          }
      }
      page_number = page_number + 1;
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
      //wrappers for grid elements
      const header = std_make('header',datum_grid);
  
  
      const expand_button = std_make('expand-button',header, {tag: 'button'});
      expand_button.innerHTML = 'v';
      //data to display
      const summary = std_make('Summary',header,{content: d['Summary']})
      const mediaOutlet = std_make('MediaOutlet',header,{content:d['MediaOutlet']})
      
  
      datum_grid.onclick = function () {
          if (!datum_grid.expanded_previously) {
  
              const name_email_wrapper = std_make('name-email-wrapper', datum_grid );
              const name_email_header = std_make('name-email-header',name_email_wrapper,{content:"Contact: ", tag: 'span'})
              const name = std_make('Name',name_email_wrapper,{content: d['Name'], tag: 'span'})
              const email = std_make('Email',name_email_wrapper,{content: d['Email'], tag: 'span'})
              
              const category = std_make('Category',datum_grid,{content:`Category: ${d['Category']}`})
  
              const date_wrapper = std_make('date-wrapper',datum_grid);
              const dateReceived = std_make('DateReceived',date_wrapper,{
                  content:("Recieved: " + d['DateReceived']), tag: 'span'
              })
              const deadline = std_make('Deadline',date_wrapper,{
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
              include_when_expanded.push(date_wrapper);
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
  /*
  function makeDropdownOption (parent, value){
      const dde = document.createElement('option'); //dropdown element
      dde.value = value;
      dde.innerHTML = value;
      parent.appendChild(dde);
  }
  
  function configDropdownMenus () {
      Categories.push('');
      for (let datum of DATA) {
          if (!Categories.includes(datum.Category) && datum.Category != "") Categories.push(datum.Category);
      }
      const category_search = document.getElementById('category-search')
      for (let category of Categories) {
          makeDropdownOption(
              category_search,
              category
          )
      }
  }*/