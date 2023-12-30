const server_url = 'http://127.0.0.1:5000';

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
function create_element(name, {className, textContent, style, id, type, children, checked, for_val}){
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
  return element;
}
