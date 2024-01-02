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
function get_prob_server(handle, user_info, submission, problem){
    fetch(`${server_url}/solve_probability`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'handle': handle,
            'problem': problem,
            'user_info': user_info,
            'submission': submission
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

// Function to get data from server
function receive_data_prob(handle, problem){
    // Receive user info
    if (handle === null){
        alert('Please login to use Qsuggest Functionality')
    }
    else{
        // Receive user info
        const user_data = fetch(`https://codeforces.com/api/user.info?handles=${handle}`, {
            method: 'GET'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            data = data['result'][0];
            return data;
        });
  
        // Receive submission info
        const submission_data = fetch(`https://codeforces.com/api/user.status?handle=${handle}`, {
            method: 'GET'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            data = data['result'];
            return data;
        });
  
        // Receive problem data
        const problem_data = fetch(`https://codeforces.com/api/problemset.problems`, {
            method: 'GET'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
        return response.json();
        })
        .then(data => {
            data = data['result'];
            return data;
        })

        // Pass the data to server
        Promise.all([user_data, submission_data, problem_data])
        .then(data => {
            for (let i = 0; i < data[2]['problems'].length; i++){
                if ((data[2]['problems'][i]['contestId'] === problem['contestId']) && 
                (data[2]['problems'][i]['index'] === problem['index'])){
                    // Creating new problem
                    const problem_val = Object.assign({}, data[2]['problems'][i], data[2]['problemStatistics'][i]);
                    keys = ['difficulty', 'points', 'rating', 'solvedCount', 'tags'];
                    nan_val = [-1, -1, -1, -1, []];
                    for (let j = 0; j < keys.length; j++){
                        problem_val[keys[j]] = (keys[j] in problem_val) ? problem_val[keys[j]] : nan_val[j];
                    }
                    get_prob_server(handle, data[0], data[1], problem_val);
                }
            }
        })
    }
}

chrome.storage.local.get(['checkbox_pred']).then((result) => {
    if (result.checkbox_pred){
        receive_data_prob(get_handle(), get_problem())
    }
})