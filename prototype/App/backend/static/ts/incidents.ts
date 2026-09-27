const url = "/api/incidents/";

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
        <td><a href="incidents_detail.html?id=${data[i].id}">View</a></td>
      </tr>`;
  }
  document.getElementById("incident-list").innerHTML = html;
}

// Create new incident
async function createIncident(e) {
  e.preventDefault();
  
  const newIncident = {
    title: (document.getElementById("title") as HTMLInputElement).value,
    description: (document.getElementById("description") as HTMLInputElement).value,
    location: (document.getElementById("location") as HTMLInputElement).value,
    severity: (document.getElementById("severity") as HTMLInputElement).value
  };

  await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newIncident)
  });

  loadIncidents();
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
    title: (document.getElementById("edit-title") as HTMLInputElement).value,
    description: (document.getElementById("edit-description") as HTMLInputElement).value,
    location: (document.getElementById("edit-location") as HTMLInputElement).value,
    severity: (document.getElementById("edit-severity") as HTMLInputElement).value
  };

  await fetch(url + id, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updated)
  });

  loadDetail();
}

// Simple page check to run appropriate function on load
if (document.getElementById("incident-list")) {
  loadIncidents();
  document.getElementById("create-form").addEventListener("submit", createIncident);
}

if (document.getElementById("incident-detail")) {
  loadDetail();
  document.getElementById("resolve-btn").addEventListener("click", resolveIncident);
  document.getElementById("edit-form").addEventListener("submit", updateIncident);
}
