function get_handle(){
    const handle = document.querySelector('#header').querySelector('.lang-chooser').childNodes[3].childNodes[1].textContent;
    return handle.trim();
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
    })
  }

  receive_data()