let teachingLevel = document.getElementById('teaching-level');  
let submitBtn = document.getElementById('submit-btn');

// Toggle some features for primary and secondary options
teachingLevel.addEventListener('change', ()=> { 
  if (teachingLevel.value == 'Secondary') {
    submitBtn.insertAdjacentHTML('beforeBegin', secondaryOptionElements)
  } else {
    let secondaryOptions = document.getElementById("secondary-options");
    if (secondaryOptions) {
        secondaryOptions.remove()
     }
  }
})

var secondaryOptionElements = `
<div class="row mt-1" id="secondary-options">
    <div class="col-md-6">
      <div class="form-group">
         <label class="text-muted">School Level</label>
         <select name="school_category" id="" class="form-select-1">  
           <option value="School category" disabled selected>Select School category</option>
           <option value="National">National</option>
           <option value="Extra County">Extra County</option>
           <option value="County">County</option>
           <option value="Sub-county">Sub-county</option>
         </select>
      </div>
    </div>
    <div class="col-md-6">
      <div class="form-group">
        <label class="text-muted">Teaching Subjects</label>
        <select name="subject_combination" id="" class="form-select-1">  
          <option value="Subject combination" disabled selected>Select Subject combination</option>
          <option value="English/Literature">English/Literature</option>
          <option value="Biology/Chemistry">Biology/Chemistry</option>
          <option value="Biology/Agriculture">Biology/Agriculture</option>
          <option value="Geography/CRE">Geography/CRE</option>
          <option value="Chemistry/Physics">Chemistry/Physics</option>
          <option value="Mathematics/Physics">Mathematics/Physics</option>
          <option value="Geography/History">Geography/History</option>
          <option value="Chemistry/Mathematics">Chemistry/Mathematics</option>
          <option value="Geography/IRE">Geography/IRE</option>
          <option value="Geography/Computer Studies">Geography/Computer Studies</option>
          <option value="Geography/Kiswahili">Geography/Kiswahili</option>
          <option value="Biology/Home Science">Biology/Home Science</option>
          <option value="Biology/Home Science">Biology/Home Science</option>
          <option value="History/Kiswahili">History/Kiswahili</option>
          <option value="Biology/Geography">Biology/Geography</option>
         </select>
      </div>
    </div>
  </div>
`
