// function to control checkbox toggle
function qsuggest_checkbox_pred(){
    const checkbox = document.getElementById('Qsuggest-status-pred');
    const val = (checkbox.checked) ? true : false;
    chrome.storage.local.set({checkbox_pred: val}).then(() => location.reload());
}

// function to update sidebar
function update_sidebar(checkbox_val){
    // Create new div for Qsuggest
    const div_qsuggest = 
        create_element('div', {
            className: 'roundbox sidebox borderTopRound', 
            id: 'Qsuggest-roundbox',
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
                            id: 'Qsuggest-status-pred',
                            type: 'checkbox',
                            checked: checkbox_val,
                            onchange: qsuggest_checkbox_pred
                        }),
                        create_element('label', {
                            for_val: 'Qsuggest-status-pred',
                            style: 'vertical-align: top',
                            textContent: ' View Qsuggest predictions'
                        })
                    ]
                })
            ]
        });

    // Inserting into sidebar
    const sidebar = document.querySelector('#sidebar');
    sidebar.insertBefore(div_qsuggest, sidebar.firstChild);
}

chrome.storage.local.get(['checkbox_pred']).then((result) => {
    update_sidebar(result.checkbox_pred);
})
