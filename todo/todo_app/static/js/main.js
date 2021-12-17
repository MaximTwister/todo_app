console.log("JavaScript Rocks!")
document.getElementById("todo_title").onkeydown=detectEnter


function detectEnter (event) {
    if (event.target.id === "todo_title" && event.which === 13) {
        event.preventDefault()
        document.getElementById('todo_title').contentEditable = "false"
        changeIcons()
        request_update_todo()
    }
}


function delTodo(event) {
    console.log("Delete Todo")
}

function btnAction(event) {
    console.log("Action from:", event.target.id)
    let pressed_button = event.target.id

    let second_button = (( pressed_button === 'edit') ? 'save' : 'edit')
    let is_area_editable = (( pressed_button === "edit") ? "true" : "false")

    document.getElementById(pressed_button).classList.toggle("not-vis")
    document.getElementById(second_button).classList.toggle("not-vis")

    toggle_content_edit_area(is_area_editable)
}


const changeIcons = () => {
    let icon_classes = ["fa-pencil-alt", "fa-check-square"]
    icon_classes.forEach((item) =>
        document.getElementById("edit_title").classList.toggle(item))
}


const editTitle = event => {
    console.log("Edit Title Toggled with: ", event)
    let todoTile = document.getElementById("todo_title")

    let is_updated_title = Boolean(document.getElementsByClassName("fa-check-square").length)
    if (is_updated_title) request_update_todo()

    changeIcons()
    todoTile.contentEditable = (!is_updated_title).toString()
    todoTile.focus()
};


function toggle_content_edit_area(is_area_editable) {
    let todoContent = document.getElementById("todo_content")
    console.log("Content Area Editable: ", is_area_editable)
    todoContent.contentEditable = is_area_editable
    if (is_area_editable === "false") request_update_todo()
    else todoContent.focus()
}

function createXHR(url, csrftoken) {
    // Creating a XHR object
    let xhr = new XMLHttpRequest()
    // Open an async connection
    xhr.open("POST", url, true)
    // Set the request header i.e. which type of content you are sending
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    // Create a state change callback
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

    // /** @type {String} */
    let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
    console.log("CSRF: ", csrftoken)

    // Converting JSON data to string and send with request
    const data = JSON.stringify({"title": todo_title, "content": todo_content })
    const xhr = createXHR(url, csrftoken)
    xhr.send(data)
}
