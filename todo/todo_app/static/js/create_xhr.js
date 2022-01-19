console.log("Create XHR JS")

function createXHR (url, csrftoken, method) {
    let xhr = new XMLHttpRequest()
    xhr.open(method, url, true)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.onreadystatechange = event => {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log("Perfect: ", event)
        } else if (xhr.readyState === 4 && xhr.status === 278) {
            const redirectURL = xhr.getResponseHeader('Location')
            console.log(`Redirect to ${redirectURL} :`, event)
            window.location.replace(redirectURL)
        } else console.log("Not really Perfect: ", event)
    }
    return xhr
}