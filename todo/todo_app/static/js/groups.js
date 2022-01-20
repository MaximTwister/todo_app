console.log("Groups JavaScript")

function toggleRequests(event, id) {
    console.log("Toggle Requests block")
    let elementID = `requests_block_${id}`
    let requests_block = document.getElementById(elementID)
    requests_block.classList.toggle("hide_requests_block")
}

function toggleSubscribers(event, id) {
    console.log("Toggle Subscribers block")
    let elementID = `subscribers_block_${id}`
    let subscribers_block = document.getElementById(elementID)
    subscribers_block.classList.toggle("hide_subscribers_block")
}

function editGroupSubscribers(group_pk, account_pk, type) {
    console.log(`${type} account: ${account_pk} group: ${group_pk}`)

    let url = `http://127.0.0.1:8000/todo/groups/${group_pk}/update/`
    let method = "PATCH"
    let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
    let data = JSON.stringify({
        "group_pk": group_pk,
        "account_pk": account_pk,
        "type": type
    })
    const xhr = createXHR(url, csrftoken, method)
    xhr.send(data)
}

function request_delete_object(event){
    let group_id = event.target.getAttribute("object_id")
    let url = `http://127.0.0.1:8000/todo/groups/${group_id}/delete/`
    let method = "POST"
    let csrftoken = document.getElementsByName("csrfmiddlewaretoken")[0].value
    const xhr = createXHR(url, csrftoken, method)
    xhr.send()
}