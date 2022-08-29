"use strict"

let enable_message = false

async function send_answer() {
    let url = BASE_URL.value
    let id = task_id.value
    let user_answer = answer.value
    answer.value = ''
    if (user_answer === "")
        return
    let response = await fetch(url + `api/check_answer/?id=${id}&answer=${user_answer}`)
    let data = await response.json()
    if (data.is_ok) {
        console.log("yes")
        done_count.innerText = Number(done_count.innerText) + 1
        input_form.innerHTML = data.message
    }
    else {
        console.log("no")
        if (!enable_message) {
            enable_message = true
            input_form.innerHTML = data.message + input_form.innerHTML
        }
    }
}
