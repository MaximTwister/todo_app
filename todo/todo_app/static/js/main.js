console.log("JavaScript Rocks!")

function btnAction(event) {
    let pressed_button = event.target.id
    console.log("Action from: ", pressed_button)

    let second_button = ((pressed_button === "edit") ? "save" : "edit")
    let is_area_editable = ((pressed_button === "edit") ? "true" : "false")

    document.getElementById(pressed_button).classList.toggle("not-vis")
    document.getElementById(second_button).classList.toggle("not-vis")

    toggle_content_edit_area(is_area_editable)
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

    let url = "update/"
    let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
    let data = JSON.stringify({"content": todo_content})
    const xhr = createXHR(url, csrftoken)
    xhr.send(data)
 }

