"use strict";
const url = "/api/incidents/";
const url_forPersonnel = "/api/personnel/";
// Load table on list page
async function loadIncidents() {
    const res = await fetch(url);
    const data = await res.json();
    let html = "";
    for (let i = 0; i < data.length; i++) {
        html += `
      <tr>
        <td>${data[i].id}</td>
        <td>${data[i].title}</td>
        <td>${data[i].location}</td>
        <td>${data[i].severity}</td>
        <td>${data[i].status}</td>
        <td><a href="incident_detail.html?id=${data[i].id}">View</a></td>
      </tr>`;
    }
    document.getElementById("incident-list").innerHTML = html;
}
// Create new incident
async function createIncident(e) {
    e.preventDefault();
    const newIncident = {
        title: document.getElementById("title").value,
        description: document.getElementById("description").value,
        location: document.getElementById("location").value,
        severity: document.getElementById("severity").value
    };
    await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newIncident)
    });
    loadIncidents();
}
// Load assigned personnel list for current incident
async function loadAssignedPersonnel(incidentId) {
    const res = await fetch(url_forPersonnel);
    const allPersonnel = await res.json();
    const assigned = allPersonnel.filter((p) => String(p.assigned_incident_id) === String(incidentId));
    const listElem = document.getElementById("assigned-personnel-list");
    if (!listElem)
        return;
    if (assigned.length === 0) {
        listElem.innerHTML = "<li>No personnel assigned yet.</li>";
        return;
    }
    let html = "";
    for (let i = 0; i < assigned.length; i++) {
        html += `<li><strong>${assigned[i].name}</strong> - ${assigned[i].role} (${assigned[i].phone})</li>`;
    }
    listElem.innerHTML = html;
}
// Populate dropdown with available personnel
async function loadAvailablePersonnelOptions() {
    const res = await fetch(url_forPersonnel);
    const allPersonnel = await res.json();
    const available = allPersonnel.filter((p) => p.status === "AVAILABLE" || !p.assigned_incident_id);
    let html = `<option value="">-- Select Personnel --</option>`;
    for (let i = 0; i < available.length; i++) {
        html += `<option value="${available[i].id}">${available[i].name} (${available[i].role})</option>`;
    }
    const selectElem = document.getElementById("personnel-select");
    if (selectElem)
        selectElem.innerHTML = html;
}
// Assign personnel to current incident
async function assignPersonnel(e) {
    e.preventDefault();
    const incidentId = new URLSearchParams(window.location.search).get("id");
    const personnelId = document.getElementById("personnel-select").value;
    if (!personnelId)
        return;
    await fetch(url_forPersonnel + personnelId, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            assigned_incident_id: incidentId,
            status: "ASSIGNED"
        })
    });
    // Reset section view and reload data
    document.getElementById("assign-personnel-section").style.display = "none";
    loadDetail();
}
// Load detail page
async function loadDetail() {
    const id = new URLSearchParams(window.location.search).get("id");
    const res = await fetch(url + id);
    const data = await res.json();
    document.getElementById("detail-title").innerText = data.title;
    document.getElementById("detail-description").innerText = data.description;
    document.getElementById("detail-location").innerText = data.location;
    document.getElementById("detail-severity").innerText = data.severity;
    document.getElementById("detail-status").innerText = data.status;
    document.getElementById("detail-created").innerText = data.created_at;
    // Pre-fill edit form
    document.getElementById("edit-title").value = data.title;
    document.getElementById("edit-description").value = data.description;
    document.getElementById("edit-location").value = data.location;
    document.getElementById("edit-severity").value = data.severity;
    // Load personnel details
    loadAssignedPersonnel(id);
    loadAvailablePersonnelOptions();
}
// Close/Resolve incident
async function resolveIncident() {
    const id = new URLSearchParams(window.location.search).get("id");
    await fetch(url + id, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: "CLOSED" })
    });
    loadDetail();
}
// Update incident
async function updateIncident(e) {
    e.preventDefault();
    const id = new URLSearchParams(window.location.search).get("id");
    const updated = {
        title: document.getElementById("edit-title").value,
        description: document.getElementById("edit-description").value,
        location: document.getElementById("edit-location").value,
        severity: document.getElementById("edit-severity").value
    };
    await fetch(url + id, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated)
    });
    document.getElementById("edit-section").style.display = "none";
    loadDetail();
}
// Page route initialization
if (document.getElementById("incident-list")) {
    loadIncidents();
    document.getElementById("create-form").addEventListener("submit", createIncident);
    document.getElementById("show-form-btn").addEventListener("click", () => {
        const section = document.getElementById("create-form-section");
        section.style.display = section.style.display === "block" ? "none" : "block";
    });
}
if (document.getElementById("incident-detail")) {
    loadDetail();
    // Button Listeners
    document.getElementById("resolve-btn").addEventListener("click", resolveIncident);
    document.getElementById("edit-btn").addEventListener("click", () => {
        const editSection = document.getElementById("edit-section");
        editSection.style.display = editSection.style.display === "block" ? "none" : "block";
    });
    const assignBtn = document.getElementById("assign-btn");
    if (assignBtn) {
        assignBtn.addEventListener("click", () => {
            const assignSection = document.getElementById("assign-personnel-section");
            assignSection.style.display = assignSection.style.display === "block" ? "none" : "block";
        });
    }
    // Form Submit Listeners
    document.getElementById("edit-form").addEventListener("submit", updateIncident);
    const assignForm = document.getElementById("assign-personnel-form");
    if (assignForm) {
        assignForm.addEventListener("submit", assignPersonnel);
    }
}
