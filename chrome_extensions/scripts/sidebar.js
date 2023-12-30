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

function update_sidebar(){
    // Create new div for Qsuggest
    const div_qsuggest = 
        create_element('div', {
            className: 'roundbox sidebox borderTopRound', 
            children: [
                create_element('div', {
                    className: 'caption titled', 
                    textContent: '→ Qsuggest', 
                    children: [
                        create_element('div', {
                            className: 'top-links'
                        })
                    ]
                }),
                create_element('div', {
                    className: 'smaller',
                    style: 'margin: 1em;',
                    children: [
                        create_element('input', {
                            id: 'Qsuggest-status',
                            type: 'checkbox',
                            checked: true
                        }),
                        create_element('label', {
                            for_val: 'Qsuggest-status',
                            style: 'vertical-align: top',
                            textContent: ' Use Qsuggest recommendations'
                        })
                    ]
                })
            ]
        });

    // Inserting into sidebar
    const sidebar = document.querySelector('#sidebar');
    sidebar.insertBefore(div_qsuggest, sidebar.firstChild);
}

update_sidebar();
  