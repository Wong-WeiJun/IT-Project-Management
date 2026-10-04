"use strict";
const url_shelters = "/api/shelters/";
function buildCapacityBar(occupied, capacity, width = 20) {
    const ratio = capacity > 0 ? occupied / capacity : 0;
    const filled = Math.round(Math.min(Math.max(ratio, 0), 1) * width);
    return "█".repeat(filled) + "░".repeat(width - filled);
}
function extractErrorMessage(err, fallback) {
    if (!err || !err.detail)
        return fallback;
    if (typeof err.detail === "string")
        return err.detail;
    if (Array.isArray(err.detail) && err.detail.length > 0) {
        return err.detail[0].msg.replace("Value error, ", "");
    }
    return fallback;
}
// Load table on list page
async function loadShelters() {
    const res = await fetch(url_shelters);
    const data = await res.json();
    let html = "";
    for (let i = 0; i < data.length; i++) {
        html += `
      <tr>
        <td>${data[i].name}</td>
        <td>${data[i].capacity}</td>
        <td>${data[i].occupied}</td>
        <td>${data[i].status}</td>
        <td><a href="shelters_detail.html?id=${data[i].id}">View</a></td>
      </tr>`;
    }
    document.getElementById("shelter-list").innerHTML = html;
}
// Create new shelter
async function createShelter(e) {
    e.preventDefault();
    const newShelter = {
        name: document.getElementById("name").value,
        location: document.getElementById("location").value,
        capacity: parseInt(document.getElementById("capacity").value, 10),
        occupied: parseInt(document.getElementById("occupied").value || "0", 10),
        status: document.getElementById("status").value
    };
    const res = await fetch(url_shelters, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newShelter)
    });
    if (!res.ok) {
        const err = await res.json().catch(() => null);
        alert(extractErrorMessage(err, "Could not add shelter."));
        return;
    }
    document.getElementById("create-form").reset();
    loadShelters();
}
async function loadShelterDetail() {
    const id = new URLSearchParams(window.location.search).get("id");
    const res = await fetch(url_shelters + id);
    const data = await res.json();
    document.getElementById("detail-name").innerText = data.name;
    document.getElementById("detail-location").innerText = data.location;
    document.getElementById("detail-status").innerText = data.status;
    document.getElementById("capacity-text").innerText = `${data.occupied} / ${data.capacity}`;
    document.getElementById("capacity-bar").innerText = buildCapacityBar(data.occupied, data.capacity);
}
// Update shelter details
async function updateShelter(e) {
    e.preventDefault();
    const id = new URLSearchParams(window.location.search).get("id");
    const updated = {
        name: document.getElementById("edit-name").value,
        location: document.getElementById("edit-location").value,
        capacity: parseInt(document.getElementById("edit-capacity").value, 10),
        occupied: parseInt(document.getElementById("edit-occupied").value, 10),
        status: document.getElementById("edit-status").value
    };
    const res = await fetch(url_shelters + id, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated)
    });
    if (!res.ok) {
        const err = await res.json().catch(() => null);
        alert(extractErrorMessage(err, "Could not save changes."));
        return;
    }
    document.getElementById("view-section").style.display = "block";
    document.getElementById("edit-section").style.display = "none";
    loadShelterDetail();
}
// Page route initialization
if (document.getElementById("shelter-list")) {
    loadShelters();
    document.getElementById("create-form").addEventListener("submit", createShelter);
    document.getElementById("show-form-btn").addEventListener("click", () => {
        const section = document.getElementById("create-form-section");
        section.style.display = section.style.display === "block" ? "none" : "block";
    });
}
if (document.getElementById("shelter-detail")) {
    loadShelterDetail();
    const editBtn = document.getElementById("edit-btn");
    if (editBtn) {
        editBtn.addEventListener("click", () => {
            document.getElementById("view-section").style.display = "none";
            document.getElementById("edit-section").style.display = "block";
        });
    }
    const editForm = document.getElementById("edit-form");
    if (editForm) {
        editForm.addEventListener("submit", updateShelter);
    }
}
