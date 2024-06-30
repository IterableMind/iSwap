let addBtn = document.getElementById('add-btn');
let itemCount = 0;

addBtn.addEventListener('click', ()=> {
  let selectedCounty = document.getElementById('counties').value;
  let selectedSubCounty = document.getElementById('sub-counties').value;

  if (selectedCounty && selectedSubCounty) {
    let table = `
    <table class="table table-bordered">
      <h6 class="text-center mt-3 text-lightred">Selected Choices</h6>
      <thead>
        <tr>
          <th>#</th>
          <th>County</th>
          <th>Sub County</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody id="table-body"></tbody>
    </table>
    `
    let selectDisplay = document.getElementsByClassName('select-display')[0];
    if (!document.getElementsByClassName('table')[0]) {
      selectDisplay.insertAdjacentHTML('afterbegin', table);
    }
    let tableBody = document.getElementById('table-body');
    let newRow = tableBody.insertRow();
    itemCount++;
    newRow.innerHTML = `
    <td>${itemCount}</td>
    <td>${selectedCounty}</td>
    <td>${selectedSubCounty}</td>
    <td class="text-danger"><i class="bi bi-trash"></i></td>
    `;
    // Disable form submission until 3 items are added
    if (tableBody.rows.length >= 3 ) {
      addBtn.remove()
      let clearSaveBtns = document.getElementById('hidden-1')
          clearSaveBtns.removeAttribute('id');
          clearSaveBtns.classList = 'd-flex justify-content-end';
    }
  } else {
    alert('Please select a county and sub-county to continue!');
  }
});
// clear inputs
let clearBtn = document.getElementById('clearbtn');
if (clearBtn) {
  clearBtn.addEventListener('click', ()=> {
    location.reload();
  });
}
// Collect selected counties and sub-counties.
const selectedPlaces = [];

document.getElementById('savebtn').addEventListener('click', () => {
  const tableBody = document.getElementById('table-body');

  for (let i = 0; i < tableBody.rows.length; i++) {
    for (let j = 1; j < tableBody.rows[i].children.length; j++) {
      const place = tableBody.rows[i].children[j].textContent.trim();

      // Ensure that the place is not empty before adding it to selectedPlaces
      if (place !== '') {
        selectedPlaces.push(place);
      }
    }
  }
 // send selected data to the backend.
  fetch('/dashboard/submitted', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(selectedPlaces)
  })
  .catch((error) => {
    console.log('Error', error);
  });
})