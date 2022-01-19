console.log("Modal JS")

let modal = document.getElementById("operationModal")

modal.addEventListener("click", function (event){
    let idAttribute = event.target.getAttribute("id")
    if (idAttribute.toLowerCase() === "modal_operation_button") delObject(event)
    else closeModal()
})

function openModal(context, operation_type, id) {
    let title_text = `${operation_type} ${context}`
    let paragraph_text = `Are we going to ${operation_type} this ${context}?`

    let paragraph = document.getElementById("modal_paragraph")
    let paragraph_text_node = document.createTextNode(paragraph_text)
    paragraph.appendChild(paragraph_text_node)

    let title = document.getElementById("modal_title")
    let title_text_node = document.createTextNode(title_text)
    title.appendChild(title_text_node)

    let operation_button = document.getElementById('modal_operation_button')
    operation_button.setAttribute('object_id', id)
    operation_button.value = operation_type.toUpperCase()

    modal.style.display = "block"
    modal.classList.add("show")
}

function delObject(event) {
    request_delete_object(event)
    closeModal()
}

function closeModal() {
    console.log("Close Modal")
    modal.style.display = "none"
    modal.classList.remove("show")
}

