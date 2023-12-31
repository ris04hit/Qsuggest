function sidebar_probability(probability){
    const element = document.querySelector('#Qsuggest-roundbox');
    element.appendChild(
        create_element('div', {
            className: 'smaller',
            style: 'margin: 1em;',
            textContent: `There is ${Math.round(100*probability)}% chance to solve this problem in first go.`
        })
    );
}

// Function to connect to Qsuggest server
function get_prob_server(handle, problem){
    fetch(`${server_url}/solve_probability`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'handle': handle,
            'problem': problem
        })
    })
    .then(response => response.json())
    .then(data => {
        sidebar_probability(data);
    })
    .catch(error => {
        console.log(error);
        alert('Can\'t connect to Qsuggest server')
      })
}

get_prob_server(get_handle(), get_problem())
