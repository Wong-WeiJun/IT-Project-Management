function formatDashboardTime(timestamp: string): string {
  const d = new Date(timestamp);
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function buildDashboardCapacityBar(occupied: number, capacity: number, width: number = 20): string {
  const ratio = capacity > 0 ? occupied / capacity : 0;
  const filled = Math.round(Math.min(Math.max(ratio, 0), 1) * width);
  return "█".repeat(filled) + "░".repeat(width - filled);
}

async function loadDashboard() {
  const [incidents, requests, personnel, shelters, resources, auditLog] = await Promise.all([
    fetch("/api/incidents/").then(r => r.json()),
    fetch("/api/requests/").then(r => r.json()),
    fetch("/api/personnel/").then(r => r.json()),
    fetch("/api/shelters/").then(r => r.json()),
    fetch("/api/resources/").then(r => r.json()),
    fetch("/api/audit/").then(r => r.json())
  ]);

  const activeIncidents = incidents.filter(i => i.status === "ACTIVE");
  document.getElementById("active-incidents-count").innerText = String(activeIncidents.length);

  const openRequests = requests.filter(r => r.status === "OPEN");
  document.getElementById("open-requests-count").innerText = String(openRequests.length);

  const availablePersonnel = personnel.filter(p => p.status === "AVAILABLE");
  document.getElementById("available-personnel-count").innerText = String(availablePersonnel.length);

  const totalAvailableResources = resources.reduce((sum, r) => sum + r.quantity_available, 0);
  document.getElementById("available-resources-count").innerText = String(totalAvailableResources);

  const totalOccupied = shelters.reduce((sum, s) => sum + s.occupied, 0);
  const totalCapacity = shelters.reduce((sum, s) => sum + s.capacity, 0);
  document.getElementById("shelter-capacity-text").innerText = `${totalOccupied} / ${totalCapacity}`;
  document.getElementById("shelter-capacity-bar").innerText = buildDashboardCapacityBar(totalOccupied, totalCapacity);

  const highPriority = requests.filter(r => r.priority === "HIGH" && r.status !== "RESOLVED");
  let hpHtml = "";
  for (let i = 0; i < highPriority.length; i++) {
    hpHtml += `<li>#${highPriority[i].id.slice(0, 4)} &mdash; ${highPriority[i].priority}</li>`;
  }
  document.getElementById("high-priority-list").innerHTML = hpHtml || "<li>None</li>";

  let incHtml = "";
  for (let i = 0; i < activeIncidents.length; i++) {
    incHtml += `
      <tr>
        <td>${activeIncidents[i].title}</td>
        <td>${activeIncidents[i].location}</td>
        <td>${activeIncidents[i].severity}</td>
        <td>${activeIncidents[i].status}</td>
      </tr>`;
  }
  document.getElementById("active-incidents-table").innerHTML = incHtml;

  const recent = auditLog.slice(0, 5);
  let activityHtml = "";
  for (let i = 0; i < recent.length; i++) {
    activityHtml += `<li>${formatDashboardTime(recent[i].timestamp)}&nbsp;&nbsp;${recent[i].user} ${recent[i].description}</li>`;
  }
  document.getElementById("recent-activity-list").innerHTML = activityHtml || "<li>No activity yet</li>";
}

if (document.getElementById("active-incidents-count")) {
  loadDashboard();
  setInterval(loadDashboard, 5000);
}
