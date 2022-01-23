const group_selector = document.getElementById("id_group")
const assignees_selector = document.getElementById("id_assignee")

group_selector.addEventListener("change",  (event) => {
    let selector = event.target
    let selectedGroupIndex = selector.selectedIndex
    let selectedGroupPK = selector.options[selectedGroupIndex].value
    console.log(`Selected Group: ${selectedGroupPK}`)
    getAssignees(selectedGroupPK)
})

function getAssignees(selectedGroupPK) {
    let url = `../../get-assignees/`
    let method = "PATCH"
    let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
    let data = JSON.stringify({
        "group_pk": selectedGroupPK,
    })
    const xhr = createXHR(url, csrftoken, method)
    console.log("Data:", data)
    xhr.send(data)
    xhr.onreadystatechange = event => {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let responseText = event.target.responseText
            let response_object = JSON.parse(responseText)
            let assignees = response_object.assignees
            console.log("Type:", typeof response_object)
            assignees_selector.innerHTML = ""
            addAssignee("", "---------", true)
            for (const [key, value] of Object.entries(assignees)) {
                console.log(`${key}: ${value}`)
                addAssignee(key, value, false)
            }
        }
    }
}

// <option value="669">Charlie</option>
function addAssignee (assigneePK, assigneeName, selected) {
    let selectOption = document.createElement('option')
    selectOption.value = assigneePK
    selectOption.innerHTML = assigneeName
    if (selected === true) {
        selectOption.selected = selected
    }
    assignees_selector.appendChild(selectOption)
}