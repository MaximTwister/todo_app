console.log("JavaScript Rocks!")
document.getElementById("todo_title").onkeydown=detectEnter


function detectEnter (event) {
    if (event.target.id === "todo_title" && event.which === 13) {
        event.preventDefault()
        let todo_title = document.getElementById("todo_title")
        todo_title.contentEditable = "false"
        todo_title.blur()
        changeIcon()
        request_update_todo()
    }
}

function delTodo(event) {
    console.log("Todo Deleted")
}

function btnAction(event) {
    let pressed_button = event.target.id
    console.log("Action from: ", pressed_button)

    let second_button = ((pressed_button === "edit") ? "save" : "edit")
    let is_area_editable = ((pressed_button === "edit") ? "true" : "false")

    document.getElementById(pressed_button).classList.toggle("not-vis")
    document.getElementById(second_button).classList.toggle("not-vis")

    toggle_content_edit_area(is_area_editable)
}

const changeIcon = () => {
    let icon_classes = ["fa-pencil-alt", "fa-check"]
    icon_classes.forEach((item) =>
        document.getElementById("edit_title").classList.toggle(item))
}

const editTitle = event => {
    console.log("Edit Title Toggled with: ", event)
    let todoTitle = document.getElementById("todo_title")
    let is_updated_title = Boolean(document.getElementsByClassName("fa-check").length)
    if (is_updated_title) request_update_todo()

    changeIcon()
    todoTitle.contentEditable = (!is_updated_title).toString()
    todoTitle.focus()
}

function toggle_content_edit_area(is_area_editable) {
    let todoContent = document.getElementById("todo_content")
    console.log("Content Area Editable: ", is_area_editable)
    todoContent.contentEditable = is_area_editable
    if (is_area_editable === "false") request_update_todo()
    else todoContent.focus()
}

function createXHR (url, csrftoken) {
    let xhr = new XMLHttpRequest()
    xhr.open("POST", url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.onreadystatechange = event => {
        if (xhr.readyState === 4 && xhr.status === 200) console.log("Perfect: ", event)
        else console.log("Not really perfect: ", event)
    }
    return xhr
}

function request_update_todo() {
    let todo_content = document.getElementById("todo_content").innerText
    let todo_title = document.getElementById("todo_title").innerText

    let url = "update/"
    let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
    let data = JSON.stringify({"title": todo_title,"content": todo_content})
    const xhr = createXHR(url, csrftoken)
    xhr.send(data)
 }
