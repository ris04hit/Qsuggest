const server_url = 'http://127.0.0.1:5000';
const num_prob_page = 100;    // Number of problems per page

// Function to get cf handle of user
function get_handle(){
  const handle_row = document.querySelector('#header').querySelector('.lang-chooser').childNodes[3];
  const login = handle_row.childNodes[3].textContent.trim();
  if (login !== "Logout"){
    return null;
  }
  const handle = handle_row.childNodes[1].textContent.trim();
  return handle;
}

// Function to get problem
function get_problem(){
  const currentUrl = window.location.href.split("/");
  const contestId = currentUrl[currentUrl.length - 2];
  const index = currentUrl[currentUrl.length - 1];
  const problem = {
    'contestId': parseInt(contestId, 10),
    'index': index
  };
  return problem;
}

// Function to create element
function create_element(name, {className, textContent, style, id, type, children, checked, for_val, href, title}){
  const element = document.createElement(name);
  if (className !== undefined){
    element.className = className;
  }
  if (textContent !== undefined){
    element.textContent = textContent;
  }
  if (style !== undefined){
    element.style = style;
  }
  if (id !== undefined){
    element.id = id;
  }
  if (type !== undefined){
    element.type = type;
  }
  if (children !== undefined){
    for (let i = 0; i < children.length; i++){
      element.appendChild(children[i]);
    }
  }
  if (checked !== undefined){
    if (checked){
      element.checked = true;
    }
    else{
      element.checked = false;
    }
  }
  if (for_val !== undefined){
    element.htmlFor = for_val;
  }
  if (href !== undefined){
    element.href = href;
  }
  if (title !== undefined);
    element.title = title;
  return element;
}

// Function to get page number
function get_pagenum(){
  const currentUrl = window.location.href.split("/");
  const pagenum = parseInt(currentUrl[currentUrl.length-1].split("?")[0], 10);
  if (isNaN(pagenum)){
    return 1;
  }
  else{
    return pagenum;
  }
}

// Function to create problem link
function create_problem_data(problem){
  return {
    'link': `/problemset/problem/${problem['contestId']}/${problem['index']}`,
    'problemId': `${problem['contestId']}${problem['index']}`,
    'name': problem['name'],
    'tags': problem['tags'],
    'submit_link': `/problemset/submit/${problem['contestId']}/${problem['index']}`,
    'rating': problem['rating'],
    'status_link': `/problemset/status/${problem['contestId']}/problem/${problem['index']}`,
    'num_solved_text': `\n&nbsp;x${problem['solvedCount']}\n`,
    'num_solved': problem['solvedCount']
  }
}

function create_tag(tag){
  return create_element('a',{
    href: `/problemset?tags=${tag}`,
    style: 'text-decoration: none;',
    className: 'notice',
    title: tag.charAt(0).toUpperCase() + tag.slice(1),
    textContent: tag
  })
}
