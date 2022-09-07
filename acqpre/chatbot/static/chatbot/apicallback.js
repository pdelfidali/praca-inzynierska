function displayMessage(text, is_user = 0) {
    const message = document.createElement('p')
    message.innerHTML = text
    if (is_user === 1) {
        message.className = 'text-end'
    } else {
        message.className = 'text-start'
    }
    let chat = document.getElementById("chat")
    chat.appendChild(message)
    chat.style.overflowY = 'scroll';
    addSeparator()
}

function sendMessage(csrfToken) {
    let user_input = document.getElementById("user_input")
    const json = {"user_input": user_input.value}
    let xhr = new XMLHttpRequest()
    displayMessage(user_input.value, 1)
    user_input.value = ''
    xhr.open('POST', '/api/')
    xhr.setRequestHeader("X-CSRFToken", csrfToken)
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onload = function () {
        if (xhr.status === 200) {
            let responseMessage = JSON.parse(this.response)
            displayMessage(responseMessage.message)
        }
    }
    xhr.send(JSON.stringify(json));
}

function addSeparator() {
    let hr = document.createElement('hr')
    document.getElementById("chat").appendChild(hr)
}