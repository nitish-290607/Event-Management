const API_BASE_URL = 'http://127.0.0.1:8000/api';

// --- Authentication & Navigation ---
function initNavigation() {
    const navLinks = document.getElementById('navLinks');
    if (!navLinks) return;

    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (token) {
        let links = `
            <li class="nav-item"><a class="nav-link" href="dashboard.html">Dashboard</a></li>
        `;
        if (role === 'Admin') {
            links += `<li class="nav-item"><a class="nav-link" href="admin.html">Admin Panel</a></li>`;
        }
        links += `<li class="nav-item"><a class="nav-link" href="#" onclick="logout()">Logout</a></li>`;
        navLinks.innerHTML = links;
    } else {
        navLinks.innerHTML = `
            <li class="nav-item"><a class="nav-link" href="login.html">Login / Register</a></li>
        `;
    }
}

async function loginUser(event) {
    event.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch(`${API_BASE_URL}/users/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ username: email, password: password })
        });

        if (!response.ok) throw new Error("Invalid credentials");
        const data = await response.json();
        
        localStorage.setItem('token', data.access_token);
        
        // Fetch User Info to get Role
        const userRes = await fetch(`${API_BASE_URL}/users/me`, {
            headers: { 'Authorization': `Bearer ${data.access_token}` }
        });
        const userData = await userRes.json();
        localStorage.setItem('role', userData.role);
        
        window.location.href = 'index.html';
    } catch (error) {
        alert(error.message);
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    window.location.href = 'index.html';
}

// --- Events Management ---
async function loadEvents() {
    const searchInput = document.getElementById('searchInput');
    const searchQuery = searchInput ? searchInput.value : '';
    let url = `${API_BASE_URL}/events/`;
    if (searchQuery) {
        url += `?search=${encodeURIComponent(searchQuery)}`;
    }

    try {
        const response = await fetch(url);
        const events = await response.json();
        const container = document.getElementById('eventsContainer');
        if (!container) return;

        container.innerHTML = '';
        if (events.length === 0) {
            container.innerHTML = '<p class="text-center">No events found.</p>';
            return;
        }

        events.forEach(event => {
            const card = `
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <img src="${event.image_url || 'https://via.placeholder.com/400x200?text=No+Image'}" class="card-img-top" alt="Event Image">
                        <div class="card-body">
                            <h5 class="card-title">${event.title}</h5>
                            <p class="card-text text-muted">${event.venue} | ${event.event_date}</p>
                            <p class="card-text">${event.description.substring(0, 100)}...</p>
                            <p class="mb-2"><strong>Capacity:</strong> ${event.current_attendees} / ${event.capacity}</p>
                            <span class="status-${event.status.toLowerCase()}">${event.status.toUpperCase()}</span>
                        </div>
                        <div class="card-footer bg-transparent border-top-0 pb-3 text-center">
                            <button class="btn btn-primary w-100" onclick="registerForEvent(${event.id}, ${event.ticket_price})">Register Now ($${event.ticket_price.toFixed(2)})</button>
                        </div>
                    </div>
                </div>
            `;
            container.innerHTML += card;
        });
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

async function registerForEvent(eventId, price) {
    const token = localStorage.getItem('token');
    if (!token) {
        alert("Please login first.");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/registrations/${eventId}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail);
        }

        alert("Successfully registered for the event! Check your dashboard for details.");
        loadEvents(); // Refresh capacities
    } catch (error) {
        alert(`Registration failed: ${error.message}`);
    }
}

// --- Dashboard Functions ---
async function loadDashboard() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    try {
        // Load Registrations
        const regRes = await fetch(`${API_BASE_URL}/registrations/my-registrations`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const regs = await regRes.json();
        const regContainer = document.getElementById('myRegistrations');
        
        if (regs.length === 0) {
            regContainer.innerHTML = '<p>You have not registered for any events yet.</p>';
        } else {
            // Need to fetch event details for each registration. In a real app, backend would embed it.
            // Our backend Pydantic schema didn't embed event details automatically due to lazy loading issues without proper joinedload.
            // Let's just list the IDs or we can modify the backend if needed, but for now we'll fetch master event list.
            const allEventsRes = await fetch(`${API_BASE_URL}/events/`);
            const allEvents = await allEventsRes.json();
            const eventsMap = {};
            allEvents.forEach(e => eventsMap[e.id] = e);

            let html = '<ul class="list-group">';
            regs.forEach(reg => {
                if(reg.status === 'registered') {
                    const eventTitle = eventsMap[reg.event_id]?.title || `Event #${reg.event_id}`;
                    const eventDate = eventsMap[reg.event_id]?.event_date || '';
                    html += `
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            <div>
                                <h5>${eventTitle}</h5>
                                <small class="text-muted">Date: ${eventDate}</small>
                            </div>
                            <button class="btn btn-danger btn-sm" onclick="cancelRegistration(${reg.event_id})">Cancel Registration</button>
                        </li>
                    `;
                }
            });
            html += '</ul>';
            regContainer.innerHTML = html;
        }

        // Load Notifications
        const notifRes = await fetch(`${API_BASE_URL}/users/notifications`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const notifs = await notifRes.json();
        const notifContainer = document.getElementById('myNotifications');
        
        if (notifs.length === 0) {
            notifContainer.innerHTML = '<p>No new notifications.</p>';
        } else {
            let html = '<ul class="list-group">';
            notifs.forEach(n => {
                html += `<li class="list-group-item">${n.message} <br><small class="text-muted">Status: ${n.is_read ? 'Read' : 'Unread'}</small></li>`;
            });
            html += '</ul>';
            notifContainer.innerHTML = html;
        }
    } catch (error) {
        console.error("Dashboard error", error);
    }
}

async function cancelRegistration(eventId) {
    if(!confirm("Are you sure you want to cancel this registration?")) return;
    
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${API_BASE_URL}/registrations/${eventId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if(response.ok) {
            alert("Registration cancelled.");
            loadDashboard();
        } else {
            const data = await response.json();
            alert(`Error: ${data.detail}`);
        }
    } catch (error) {
        alert(error.message);
    }
}
