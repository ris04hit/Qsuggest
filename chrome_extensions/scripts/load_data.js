function get_handle(){
    const handle_row = document.querySelector('#header').querySelector('.lang-chooser').childNodes[3];
    const login = handle_row.childNodes[3].textContent.trim();
    if (login !== "Logout"){
      return null;
    }
    const handle = handle_row.childNodes[1].textContent.trim();
    return handle;
  }
  
function filter_data(data){
  return data;
}
  
function receive_data(){
  fetch('http://127.0.0.1:5000/get_data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({handle: get_handle()})
  })
  .then(response => response.json())
  .then(data => {
    console.log("Received flask data:", data);
    console.log("Filtered data:", filter_data(data));
  })
}

receive_data()