document.addEventListener('DOMContentLoaded', function() {

  if (dynamics > 0) {
    document.querySelector('#sharepage-dynamics').className = 'green';
  }
  else if (dynamics < 0) {
    document.querySelector('#sharepage-dynamics').className = 'red';
  }

  document.querySelector('#change-price').addEventListener('click', () => show_form());

  document.querySelector('#edit-notes').addEventListener('click', () => edit_notes());
})

function show_form() {
  document.querySelector('#sharepage-priceinfo').style.display = 'none';
  document.querySelector('#change-price').style.display = 'none';
  document.querySelector('#sharepage-form-changeprice').style.display = 'flex';
}

function edit_notes() {
  console.log(document.querySelector('#sharepage-notes-text').value)
  fetch(`/share/${share}/editnotes`, {
    method: 'POST',
    body: JSON.stringify({
      notes: document.querySelector('#sharepage-notes-text').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
}