// Function to hide table
function hide_table(){
  const table = document.querySelector('.problems').querySelector('tbody');
  table.style.display = 'none';
}

// Function to show table
function show_table(){
  const table = document.querySelector('.problems').querySelector('tbody');
  table.style.display = '';
}

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
      const new_problem_data = create_problem_data(problem_data[pid]);
      const element = [prob_adv[pid], new_problem_data];
      filtered_data.push(element);
    }
  }
  
  // Sorting filtered data
  filtered_data.sort((a, b) => b[0] - a[0]);

  return filtered_data;
}

// Function to modify a row in table
function modify_row(row, problem){
  const data = row.querySelectorAll('td');

  // Modifying first column
  data[0].querySelector('a').href = problem['link'];
  data[0].querySelector('a').textContent = problem['problemId'];

  // Modifying second column
  const name = data[1].querySelectorAll('div');
  name[0].querySelector('a').href = problem['link'];
  name[0].querySelector('a').textContent = problem['name'];
  name[1].innerHTML = '';
  for (let i=0; i<problem['tags'].length; i++){
    if (i != 0){
      name[1].innerHTML += '\n, \n';
    }
    name[1].appendChild(create_tag(problem['tags'][i]));
  }

  // Modifying third column
  const action = data[2].querySelectorAll('span')
  action[0].querySelector('a').href = problem['submit_link'];
  action[1].remove();

  // Modifying fourth column
  if (problem['rating'] === -1){
    data[3].innerHTML = '';
  }
  else{
    if (data[3].querySelector('span') !== null){
      data[3].querySelector('span').textContent = problem['rating'];
    }
    else{
      data[3].appendChild(create_element('span', {
        title: 'Difficulty',
        className: 'ProblemRating',
        textContent: problem['rating']
      }));
    }
  }

  // Modifying fifth column
  const status = data[4].querySelector('a');
  status.href = problem['status_link'];
  status.childNodes[1].remove();
  status.innerHTML += problem['num_solved_text'];
}

// Function to show data in table
function modify_table(paged_data){
  const table = document.querySelector('.problems').querySelector('tbody');
  const rows = table.querySelectorAll('tr');
  for (let i = paged_data.length + 1; i < rows.length; i++){
    rows[i].remove();
  }
  for (let i = 0; i < paged_data.length; i++){
    modify_row(rows[i+1], paged_data[i][1]);
  }

  show_table();
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
    const filtered_data = filter_data(data);
    const page_num = get_pagenum();
    const paged_data = filtered_data.slice(num_prob_page*(page_num-1), num_prob_page*page_num);
    modify_table(paged_data);
  })
  .catch(error => {
    console.log(error);
    alert('Can\'t connect to Qsuggest server')
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
      get_data_server(send_data);
    })
  }
}

chrome.storage.local.get(['checkbox_sug']).then((result) => {
  if (result.checkbox_sug){
    hide_table()
    receive_data(get_handle())
  }
})