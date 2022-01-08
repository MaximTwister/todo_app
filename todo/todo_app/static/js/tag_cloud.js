console.log("STARTED")
let tags_list = document.getElementById('tag_container')
let tag_text = tags_list.innerHTML.replace(/<.*?>/g," ").replace(/ +/g," ")

let tags = tag_text.split(';')

for (element of tags){
    let newTag = document.createElement('div')
    newTag.className = 'item'
    newTag.id = element
    let a = document.createElement('a')

    a.setAttribute('href', '#')
    a.textContent = element

    document.getElementById('list_id').appendChild(newTag);
    document.getElementById(element).appendChild(a);

    newTag.addEventListener('click', () => widget_handler(newTag, true))
}



[...document.querySelectorAll('.item')].forEach(function(item) {
    item.addEventListener('click', function() {
        let selected_tag = item.cloneNode(true)
        selected_tag.className = 'selected';
        selected_tag.firstChild.insertAdjacentHTML("beforeend", '<button class="remove-button">[x]</button>');
        selected_tag.firstChild.addEventListener('click', function(){
            selected_tag.remove()
            item.className = 'item'
            widget_handler(selected_tag, false)
        })
        let form = document.getElementById('form_id')
        let child = document.getElementById(item.id)
        if (form.contains(child)=== false ){
            form.appendChild(selected_tag)
            item.className ='selected'
        }
    })
})


function widget_handler(tag, bool){
    let selected = document.querySelector('.tag_widget').getElementsByTagName('option')
    for (let select of selected) {
        if (select.textContent === tag.id.replace(/\s/g, '')) { select.selected = bool}
    }
}

let widget = document.querySelector('.tag_widget')
widget.style.display = 'none'