const url_personnel = "/api/personnel/";

// Load table on list page (Section 5.2 layout: Name | Role | Status | Incident | Action)
async function loadPersonnel() {
  const res = await fetch(url_personnel);
  const data = await res.json();
  
  let html = "";
  for (let i = 0; i < data.length; i++) {
    html += `
      <tr>
        <td>${data[i].name}</td>
        <td>${data[i].role || '-'}</td>
        <td>${data[i].status}</td>
        <td>${data[i].incident_title || data[i].assigned_incident_id || '-'}</td>
        <td><a href="personnel_detail.html?id=${data[i].id}">View</a></td>
      </tr>`;
  }
  document.getElementById("personnel-list").innerHTML = html;
}

// Populate an incident dropdown for assigning personnel (used on both the
// create form and the edit form)
async function populateIncidentDropdown(selectId: string) {
  const dropdown = document.getElementById(selectId);
  if (!dropdown) return;

  const res = await fetch("/api/incidents/");
  const data = await res.json();

  let html = `<option value="">None (Unassigned)</option>`;
  for (let i = 0; i < data.length; i++) {
    html += `<option value="${data[i].id}">${data[i].title} - ${data[i].location}</option>`;
  }
  dropdown.innerHTML = html;
}

// Create new Personnel
async function createPersonnel(e) {
  e.preventDefault();
  
  const incidentVal = (document.getElementById("assigned_incident_id") as HTMLInputElement).value;

  const newPersonnel = {
    name: (document.getElementById("name") as HTMLInputElement).value,
    role: (document.getElementById("role") as HTMLInputElement).value,
    contact: (document.getElementById("contact") as HTMLInputElement).value,
    assigned_incident_id: incidentVal !== "" ? incidentVal : null
  };

  await fetch(url_personnel, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newPersonnel)
  });

  loadPersonnel();
}

// Load detail page
async function loadPersonnelDetail() {
  const id = new URLSearchParams(window.location.search).get("id");
  const res = await fetch(url_personnel + id);
  const data = await res.json();

  document.getElementById("detail-name").innerText = data.name;
  document.getElementById("detail-role").innerText = data.role || 'N/A';
  document.getElementById("detail-contact").innerText = data.contact;
  document.getElementById("detail-status").innerText = data.status;
  document.getElementById("detail-incident").innerText = data.incident_title || data.assigned_incident_id || 'Unassigned';

  populateIncidentDropdown("edit-assigned-incident-id");
}

// Set status to UNAVAILABLE
async function markUnavailable() {
  const id = new URLSearchParams(window.location.search).get("id");
  await fetch(url_personnel + id, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: "UNAVAILABLE" })
  });
  loadPersonnelDetail();
}

// Update personnel details
async function updatePersonnel(e) {
  e.preventDefault();
  const id = new URLSearchParams(window.location.search).get("id");
  
  const updated = {
    name: (document.getElementById("edit-name") as HTMLInputElement).value,
    role: (document.getElementById("edit-role") as HTMLInputElement).value,
    contact: (document.getElementById("edit-contact") as HTMLInputElement).value,
    status: (document.getElementById("edit-status") as HTMLInputElement).value,
    assigned_incident_id: (document.getElementById("edit-assigned-incident-id") as HTMLInputElement).value || null,
  };

  await fetch(url_personnel + id, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updated)
  });

  loadPersonnelDetail();
}

// Page route initialization
if (document.getElementById("personnel-list")) {
  loadPersonnel();
  populateIncidentDropdown("assigned_incident_id");
  document.getElementById("create-form").addEventListener("submit", createPersonnel);

  // Form Toggle Listener
  document.getElementById("show-form-btn").addEventListener("click", () => {
    const section = document.getElementById("create-form-section");
    section.style.display = section.style.display === "block" ? "none" : "block";
  });
}

if (document.getElementById("personnel-detail")) {
  loadPersonnelDetail();
  
  const unavailableBtn = document.getElementById("unavailable-btn");
  if (unavailableBtn) {
    unavailableBtn.addEventListener("click", markUnavailable);
  }

  const editBtn = document.getElementById("edit-btn");
  if (editBtn) {
    editBtn.addEventListener("click", () => {
      document.getElementById("edit-section").style.display = "block";
    });
  }

  const editForm = document.getElementById("edit-form");
  if (editForm) {
    editForm.addEventListener("submit", updatePersonnel);
  }
}
