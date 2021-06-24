$(document).ready(() => {
  $('#addItem').on('click', () => {
    $('#addForm').slideToggle();
  })
})

const listContainer = document.getElementById('listContainer');

const renderList = (list) => {
    listContainer.innerHTML = '';
    list.forEach(element => {

      const newItem = document.createElement('div');
      const itemName = element.item;
      newItem.className = 'itemBox';
      newItem.innerHTML = `<h2 class="itemName">${itemName}</h2>
        <p>- ${element.note}</p>
        <button class="deleteButton" onclick="deleteItem('${itemName}')">X</button>`;
      listContainer.appendChild(newItem);
    });
}

const deleteItem =  (item) => {
  fetch(`/api/delete/${item}`, {method:'DELETE'})
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      renderError(response);
    }
  })
  .then(response => {
    console.log(response)
    renderList(response);
  });
};

const getList = () => {
    fetch('/api/list')
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      renderError(response);
    }
  })
  .then(response => {
    renderList(response);
  });
}

const addItem = () => {
  let newName = document.getElementById('addName').value;
  let newNote = document.getElementById('addNote').value;

  if (newName !== '') {
    fetch(`/api/add?item=${newName}&note=${newNote}`, {method:'POST'})
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      renderError(response);
    }
  })
  .then(response => {
    renderList(response);
    document.getElementById('addName').value = '';
    document.getElementById('addNote').value = '';
  });
  }
}
getList();

