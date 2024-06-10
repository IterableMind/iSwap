let selected_county = document.getElementById('counties');
let selectElement = document.getElementById('sub-counties');

selected_county.addEventListener('change', ()=> {
  // fetch subcounties data
  fetch('/dashboard/fetchsubcounties').then(response => { 
    return response.json();
  }).then(data => {2
    // Clear options fields
    selectElement.innerHTML = '';
    for(let i = 0; i < data.length; i++) { 
      if (data[i].county == selected_county.value) { 
        data[i]['sub-counties'].forEach(item => {
          let optionElement = document.createElement('option')
          // optionElement.setAttribute('value', item)
          optionElement.value = item;
          optionElement.textContent = item;
          selectElement.appendChild(optionElement)
        });
      }
    }
  }).catch((err)=> {
    console.log('Reject', err)
  })
})