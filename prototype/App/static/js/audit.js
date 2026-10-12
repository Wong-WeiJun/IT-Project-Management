"use strict";
const url_audit = "/api/audit/";
function formatTime(timestamp) {
    const d = new Date(timestamp);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}
// Load the audit table
async function loadAuditLog() {
    const res = await fetch(url_audit);
    const data = await res.json();
    let html = "";
    for (let i = 0; i < data.length; i++) {
        html += `
      <tr>
        <td>${formatTime(data[i].timestamp)}</td>
        <td>${data[i].user}</td>
        <td>${data[i].action}</td>
        <td>${data[i].description}</td>
      </tr>`;
    }
    document.getElementById("audit-list").innerHTML = html;
}
// Page route initialization
if (document.getElementById("audit-list")) {
    loadAuditLog();
    setInterval(loadAuditLog, 5000);
}
