// Function to filter data
function filter_data(data){
  // Unpacking data
  const base_prob = data['base_probability'];
  const prob_adv = data['probability_advantage'];
  const solved_prob = new Set(data['solved_problem']);
  const problem_data = data['problem_data'];

  // Calculating relevant constants
  const num_problem = base_prob.length;

  // Calculating filter data
  var filtered_data = [];
  for (let pid = 0; pid < num_problem; pid++){
    if (!solved_prob.has(pid)){
      const element = [prob_adv[pid], problem_data['contestId'][pid], problem_data['index'][pid]];
      filtered_data.push(element);
    }
  }
  
  // Sorting filtered data
  filtered_data.sort((a, b) => b[0] - a[0]);

  return filtered_data;
}

// Function to connect to Qsuggest server
function get_data_server(data){
  fetch(`${server_url}/get_data`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    console.log("Received flask data:", data);
    console.log("Filtered data:", filter_data(data));
  })
}

// Function to get data from server
function receive_data(handle){
  // Receive user info
  if (handle === null){
    alert('Please login to use Qsuggest Functionality')
  }
  else{
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

    // Pass the data to server
    Promise.all([user_data, submission_data])
    .then(data => {
      send_data = {
        'handle': handle,
        'user_info': data[0],
        'submission': data[1]
      };
      get_data_server(send_data)
    })
  }
}

receive_data(get_handle())