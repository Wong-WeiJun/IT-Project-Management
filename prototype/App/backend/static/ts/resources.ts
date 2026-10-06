const url_resources = "/api/resources/";

let allocatingResourceId: string | null = null;

function extractResourceErrorMessage(err: any, fallback: string): string {
  if (!err || !err.detail) return fallback;
  if (typeof err.detail === "string") return err.detail;
  if (Array.isArray(err.detail) && err.detail.length > 0) {
    return err.detail[0].msg.replace("Value error, ", "");
  }
  return fallback;
}

// Populate the incident dropdown used when allocating a resource
async function populateResourceIncidentDropdown(selectId: string) {
  const dropdown = document.getElementById(selectId);
  if (!dropdown) return;

  const res = await fetch("/api/incidents/");
  const data = await res.json();

  let html = `<option value="">Select an incident</option>`;
  for (let i = 0; i < data.length; i++) {
    html += `<option value="${data[i].id}">${data[i].title} - ${data[i].location}</option>`;
  }
  dropdown.innerHTML = html;
}

async function loadResources() {
  const res = await fetch(url_resources);
  const data = await res.json();

  let html = "";
  for (let i = 0; i < data.length; i++) {
    html += `
      <tr>
        <td>${data[i].name}</td>
        <td>${data[i].quantity_total}</td>
        <td>${data[i].quantity_available}</td>
        <td>${data[i].quantity_allocated}</td>
        <td><button onclick="openAllocateForm('${data[i].id}', '${data[i].name}', ${data[i].quantity_available})">Allocate</button></td>
      </tr>`;
  }
  document.getElementById("resource-list").innerHTML = html;
}

// Create new resource
async function createResource(e) {
  e.preventDefault();

  const newResource = {
    name: (document.getElementById("name") as HTMLInputElement).value,
    category: (document.getElementById("category") as HTMLInputElement).value,
    quantity_total: parseInt((document.getElementById("quantity_total") as HTMLInputElement).value, 10)
  };

  const res = await fetch(url_resources, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newResource)
  });

  if (!res.ok) {
    const err = await res.json().catch(() => null);
    alert(extractResourceErrorMessage(err, "Could not add resource."));
    return;
  }

  (document.getElementById("create-form") as HTMLFormElement).reset();
  loadResources();
}

function openAllocateForm(id: string, name: string, available: number) {
  allocatingResourceId = id;
  document.getElementById("allocate-resource-name").innerText = `${name} (${available} available)`;
  (document.getElementById("allocate-quantity") as HTMLInputElement).value = "";
  document.getElementById("allocate-section").style.display = "block";
  populateResourceIncidentDropdown("allocate-incident");
}

// Submit an allocation
async function allocateResource(e) {
  e.preventDefault();

  const quantity = parseInt((document.getElementById("allocate-quantity") as HTMLInputElement).value, 10);
  const incidentId = (document.getElementById("allocate-incident") as HTMLSelectElement).value;

  const res = await fetch(`${url_resources}${allocatingResourceId}/allocate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ quantity: quantity, incident_id: incidentId })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => null);
    alert(extractResourceErrorMessage(err, "Could not allocate resource."));
    return;
  }

  document.getElementById("allocate-section").style.display = "none";
  loadResources();
}

// Page route initialization
if (document.getElementById("resource-list")) {
  loadResources();
  document.getElementById("create-form").addEventListener("submit", createResource);
  document.getElementById("allocate-form").addEventListener("submit", allocateResource);

  document.getElementById("show-form-btn").addEventListener("click", () => {
    const section = document.getElementById("create-form-section");
    section.style.display = section.style.display === "block" ? "none" : "block";
  });
}
