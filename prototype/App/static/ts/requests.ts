const url_request = "/api/requests/";

// Load table on list page
async function loadRequests() {
  const res = await fetch(url_request);
  const data = await res.json();
  
  let html = "";
  for (let i = 0; i < data.length; i++) {
    html += `
      <tr>
        <td>${data[i].id}</td>
        <td>${data[i].requester_name}</td>
        <td>${data[i].location}</td>
        <td>${data[i].priority}</td>
        <td>${data[i].status}</td>
        <td>${data[i].incident_id}</td>
        <td><a href="requests_detail.html?id=${data[i].id}">View</a></td>
      </tr>`;
  }
  document.getElementById("request-list").innerHTML = html;
}

async function loadIncidentOptions() {
  const res = await fetch("/api/incidents/");
  const data = await res.json();

  let html = `<option value="">Select an incident</option>`;
  for (let i = 0; i < data.length; i++) {
    html += `<option value="${data[i].id}">${data[i].title} - ${data[i].location}</option>`;
  }
  document.getElementById("incident").innerHTML = html;
}

// Create new Requests
async function createRequest(e) {
  e.preventDefault();
  
  const newRequest = {
    incident_id: (document.getElementById("incident") as HTMLInputElement).value,
    requester_name: (document.getElementById("requester") as HTMLInputElement).value,
    requester_contact: (document.getElementById("contact") as HTMLInputElement).value,
    description: (document.getElementById("description") as HTMLInputElement).value,
    location: (document.getElementById("location") as HTMLInputElement).value,
    priority: (document.getElementById("priority") as HTMLInputElement).value
  };

  await fetch(url_request, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newRequest)
  });

  loadRequests();
}

// Load detail page
async function loadRequestDetail() {
  const id = new URLSearchParams(window.location.search).get("id");
  const res = await fetch(url_request + id);
  const data = await res.json();

  document.getElementById("detail-requester").innerText = data.requester_name;
  document.getElementById("detail-contact").innerText = data.requester_contact;
  document.getElementById("detail-description").innerText = data.description;
  document.getElementById("detail-location").innerText = data.location;
  document.getElementById("detail-priority").innerText = data.priority;
  document.getElementById("detail-status").innerText = data.status;
  document.getElementById("detail-incident-id").innerText = data.incident_id;
  document.getElementById("detail-created").innerText = data.created_at;
}

// Close/Resolve Request
async function resolveRequest() {
  const id = new URLSearchParams(window.location.search).get("id");
  await fetch(url_request + id, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: "RESOLVED" })
  });
  loadRequestDetail();
}

// Update request
async function updateRequest(e) {
  e.preventDefault();
  const id = new URLSearchParams(window.location.search).get("id");
  
  const updated = {
    requester_name: (document.getElementById("edit-requester-name") as HTMLInputElement).value,
    requester_contact: (document.getElementById("edit-requester-contact") as HTMLInputElement).value,
    description: (document.getElementById("edit-description") as HTMLInputElement).value,
    location: (document.getElementById("edit-location") as HTMLInputElement).value,
    priority: (document.getElementById("edit-priority") as HTMLInputElement).value,
    status: (document.getElementById("edit-status") as HTMLInputElement).value,
  };

  await fetch(url_request + id, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updated)
  });

  loadRequestDetail();
}

// Simple page check to run appropriate function on load
if (document.getElementById("request-list")) {
  loadRequests();
  loadIncidentOptions();
  document.getElementById("create-form").addEventListener("submit", createRequest);

  // Form Toggle Listener
  document.getElementById("show-form-btn").addEventListener("click", () => {
    const section = document.getElementById("create-form-section");
    section.style.display = section.style.display === "block" ? "none" : "block";
  });
}

if (document.getElementById("request-detail")) {
  loadRequestDetail();
  document.getElementById("resolve-btn").addEventListener("click", resolveRequest);
  document.getElementById("edit-btn").addEventListener("click", () => {
    document.getElementById("edit-section").style.display = "block";
  });
  document.getElementById("edit-form").addEventListener("submit", updateRequest);
}
