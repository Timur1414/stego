"use strict"

async function send_answer() {
    let url = BASE_URL.value
    let id = task_id.value
    let user_answer = answer.value
    if (user_answer === "")
        return
    let response = await fetch(url + `api/check_answer/?id=${id}&answer=${user_answer}`)
    let data = await response.json()
    if (data.is_ok) {
        console.log("yes")
        input_form.remove()
    }
    else {
        console.log("no")
    }
}
