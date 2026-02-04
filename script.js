function loadTasks() {
    fetch("/get_tasks")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("taskList");
            list.innerHTML = "";
            data.forEach(task => {
                list.innerHTML += `
                    <li class="${task.completed ? 'completed' : ''}">
                        ${task.task}
                        <button onclick="toggleTask(${task.id})">✔</button>
                    </li>
                `;
            });
        });
}

function addTask() {
    const input = document.getElementById("taskInput");
    fetch("/add_task", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({task: input.value})
    }).then(() => {
        input.value = "";
        loadTasks();
    });
}

function toggleTask(id) {
    fetch(`/toggle/${id}`, {method: "PUT"})
        .then(() => loadTasks());
}

// ---- DIARY ----
function loadDiary() {
    fetch("/get_diary")
        .then(res => res.json())
        .then(data => {
            const div = document.getElementById("diaryEntries");
            div.innerHTML = "";
            data.forEach(d => {
                div.innerHTML += `
                    <div class="diary-entry">
                        <small>${d.date}</small>
                        <p>${d.entry}</p>
                    </div>
                `;
            });
        });
}

function addDiary() {
    const input = document.getElementById("diaryInput");
    fetch("/add_diary", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({entry: input.value})
    }).then(() => {
        input.value = "";
        loadDiary();
    });
}

loadTasks();
loadDiary();
