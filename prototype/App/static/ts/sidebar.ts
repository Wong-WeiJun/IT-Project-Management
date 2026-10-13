const sidebarLinks = [
  { key: "dashboard", label: "Dashboard", href: "/dashboard.html", adminOnly: false },
  { key: "incidents", label: "Incidents", href: "/incidents.html", adminOnly: false },
  { key: "requests", label: "Requests", href: "/requests.html", adminOnly: false },
  { key: "personnel", label: "Personnel", href: "/personnel.html", adminOnly: false },
  { key: "shelters", label: "Shelters", href: "/shelters.html", adminOnly: false },
  { key: "resources", label: "Resources", href: "/resources.html", adminOnly: false },
  { key: "audit", label: "Audit Log", href: "/audit.html", adminOnly: true }
];

function currentSectionKey(): string {
  const path = window.location.pathname;
  if (path === "/") return "dashboard";
  return path.replace("/", "").replace("_detail", "").replace(".html", "");
}

async function fetchCurrentUser(): Promise<{ username: string; role: string } | null> {
  const res = await fetch("/api/auth/me");
  if (!res.ok) return null;
  return res.json();
}

async function buildSidebar() {
  const user = await fetchCurrentUser();
  const style = document.createElement("style");
  style.textContent = `
    #app-sidebar {
      position: fixed;
      top: 0;
      left: 0;
      bottom: 0;
      width: 170px;
      padding: 1rem 0;
      border-right: 1px solid;
      box-sizing: border-box;
      font-family: Arial, sans-serif;
      overflow-y: auto;
    }
    #app-sidebar .sidebar-title {
      padding: 0 1rem 1rem 1rem;
      font-weight: bold;
      font-size: 0.9rem;
    }
    #app-sidebar .sidebar-user {
      padding: 0 1rem 1rem 1rem;
      font-size: 0.8rem;
    }
    #app-sidebar button {
      display: block;
      width: 100%;
      text-align: left;
      padding: 0.6rem 1rem;
      border: none;
      background: none;
      font-size: 1rem;
      cursor: pointer;
      box-sizing: border-box;
    }
    #app-sidebar button:hover {
      background: rgba(0, 0, 0, 0.05);
    }
    #app-sidebar button.active {
      font-weight: bold;
      border-left: 3px solid;
      background: rgba(0, 0, 0, 0.08);
    }
    body {
      margin-left: 170px;
    }
  `;
  document.head.appendChild(style);

  const nav = document.createElement("nav");
  nav.id = "app-sidebar";

  const activeKey = currentSectionKey();
  const links = sidebarLinks.filter(link => !link.adminOnly || (user && user.role === "admin"));

  let html = `<div class="sidebar-title">GLIZZY ESCS</div>`;
  if (user) {
    html += `<div class="sidebar-user">${user.username} (${user.role})</div>`;
  }
  for (let i = 0; i < links.length; i++) {
    const link = links[i];
    const activeClass = link.key === activeKey ? "active" : "";
    html += `<button class="${activeClass}" onclick="window.location.href='${link.href}'">${link.label}</button>`;
  }
  html += `<button onclick="window.location.href='/logout'">Log out</button>`;
  nav.innerHTML = html;

  document.body.prepend(nav);
}

buildSidebar();
