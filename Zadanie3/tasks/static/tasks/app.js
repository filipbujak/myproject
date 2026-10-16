// ===== elementy strony =====
const form = document.getElementById("task-form");
const input = document.getElementById("task-title");
const list = document.getElementById("task-list");
const message = document.getElementById("message");
const countAll = document.getElementById("count-all");
const countDone = document.getElementById("count-done");
const filterButtons = document.querySelectorAll("[data-filter]");

// ===== stan aplikacji =====
let tasks = [];            // wszystkie zadania z serwera
let currentFilter = "all"; // "all" | "active" | "completed"


// ===== pomocnicze =====
function showMessage(text) {
    message.textContent = text;
}

function getCsrfToken() {
    // token wstawiony przez {% csrf_token %} w formularzu
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

// wspólna funkcja do komunikacji z API
async function apiRequest(url, method = "GET", body = null) {
    const options = {
        method: method,
        headers: { "X-CSRFToken": getCsrfToken() },
    };

    if (body !== null) {
        options.headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);
    const data = await response.json();

    // fetch nie rzuca błędu przy 4xx/5xx, więc sprawdzamy sami
    if (!response.ok) {
        throw new Error(data.error || "Wystąpił błąd serwera");
    }
    return data;
}


// ===== pobieranie =====
async function loadTasks() {
    try {
        tasks = await apiRequest("/api/tasks/");
        renderTasks();
    } catch (error) {
        showMessage("Nie udało się pobrać zadań: " + error.message);
    }
}


// ===== renderowanie =====
function getVisibleTasks() {
    if (currentFilter === "active") {
        return tasks.filter(task => !task.completed);
    }
    if (currentFilter === "completed") {
        return tasks.filter(task => task.completed);
    }
    return tasks;
}

function createTaskElement(task) {
    const li = document.createElement("li");
    if (task.completed) {
        li.classList.add("completed");
    }

    const title = document.createElement("span");
    title.className = "title";
    title.textContent = task.title; // textContent, nie innerHTML

    const toggleButton = document.createElement("button");
    toggleButton.type = "button";
    toggleButton.textContent = task.completed ? "Przywróć" : "Ukończ";
    toggleButton.addEventListener("click", () => toggleTask(task));

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.textContent = "Usuń";
    deleteButton.addEventListener("click", () => deleteTask(task.id));

    li.append(title, toggleButton, deleteButton);
    return li;
}

function updateSummary() {
    countAll.textContent = tasks.length;
    countDone.textContent = tasks.filter(task => task.completed).length;
}

function renderTasks() {
    list.replaceChildren(); // czyści listę

    const visible = getVisibleTasks();
    for (const task of visible) {
        list.appendChild(createTaskElement(task));
    }

    if (visible.length === 0) {
        const empty = document.createElement("li");
        empty.textContent = "Brak zadań.";
        list.appendChild(empty);
    }

    updateSummary();
}


// ===== operacje =====
async function addTask(event) {
    event.preventDefault(); // blokuje przeładowanie strony

    const title = input.value.trim();
    if (title === "") {
        showMessage("Zadanie nie może być puste.");
        return;
    }

    try {
        await apiRequest("/api/tasks/", "POST", { title: title });
        input.value = "";
        showMessage("");
        await loadTasks();
    } catch (error) {
        showMessage("Nie udało się dodać zadania: " + error.message);
    }
}

async function toggleTask(task) {
    try {
        await apiRequest(`/api/tasks/${task.id}/`, "PATCH", { completed: !task.completed });
        showMessage("");
        await loadTasks();
    } catch (error) {
        showMessage("Nie udało się zmienić statusu: " + error.message);
    }
}

async function deleteTask(id) {
    try {
        await apiRequest(`/api/tasks/${id}/`, "DELETE");
        showMessage("");
        await loadTasks();
    } catch (error) {
        showMessage("Nie udało się usunąć zadania: " + error.message);
    }
}

function setFilter(event) {
    currentFilter = event.target.dataset.filter;

    filterButtons.forEach(button => button.classList.remove("active"));
    event.target.classList.add("active");

    renderTasks(); // bez pytania serwera, filtrujemy to, co już mamy
}


// ===== start =====
form.addEventListener("submit", addTask);
filterButtons.forEach(button => button.addEventListener("click", setFilter));
loadTasks();