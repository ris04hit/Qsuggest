function update_sidebar(){
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
