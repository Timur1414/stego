"user strict"

let ALL_TASKS = tasks.innerHTML
let timer = setTimeout(1000)
let url = BASE_URL.value

async function find() {
    tasks.innerHTML = "<p>Поиск</p>"
    let title = search_input.value
    if (title === "")
        tasks.innerHTML = ALL_TASKS
    else {
        let response = await fetch(url + `api/tasks_search/?title=${title}`)
        let data = await response.json()
        tasks.innerHTML = data.html
    }
}

function search() {
    clearTimeout(timer)
    timer = setTimeout(find, 500)
}
