const API_URL = "http://127.0.0.1:8000";


// =========================================
// SEARCH SERVICES
// =========================================

function searchServices() {

    const search =
        document.getElementById("searchInput");

    if (!search) return;

    const value =
        search.value.trim();

    if (!value) {

        alert("Please enter a service");

        return;
    }

    window.location.href =
        `services.html?search=${encodeURIComponent(value)}`;
}



// =========================================
// OPEN SERVICE
// =========================================

function openService(service) {

    window.location.href =
        `services.html?search=${encodeURIComponent(service)}`;

}



// =========================================
// LOAD SERVICES
// =========================================

async function loadServices() {

    try {

        const response =
            await fetch(
                `${API_URL}/services/`
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load services"
            );

        }


        const services =
            await response.json();


        return services;

    }

    catch (error) {

        console.error(
            "Service error:",
            error
        );

        return [];

    }

}



// =========================================
// GET USER FROM TOKEN
// =========================================

function getUserFromToken() {

    const token =
        localStorage.getItem(
            "access_token"
        );


    if (!token) {
        return null;
    }


    try {

        const payload =
            JSON.parse(
                atob(
                    token.split(".")[1]
                )
            );


        return payload;

    }

    catch (error) {

        console.error(
            "Invalid token:",
            error
        );


        return null;

    }

}



// =========================================
// LOGOUT
// =========================================

function logout() {

    localStorage.removeItem(
        "access_token"
    );


    window.location.href =
        "login.html";

}



// =========================================
// UPDATE NAVIGATION
// =========================================

function updateNavigation() {

    const token =
        localStorage.getItem(
            "access_token"
        );


    const navLinks =
        document.querySelector(
            ".nav-links"
        );


    if (!navLinks) {
        return;
    }


    if (token) {

        navLinks.innerHTML = `

            <a href="index.html">
                Home
            </a>

            <a href="services.html">
                Services
            </a>

            <a href="bookings.html">
                My Bookings
            </a>

            <a href="#" onclick="logout()">
                Logout
            </a>

        `;

    }

    else {

        navLinks.innerHTML = `

            <a href="index.html">
                Home
            </a>

            <a href="services.html">
                Services
            </a>

            <a href="login.html">
                Login
            </a>

            <a href="register.html">
                Register
            </a>

        `;

    }

}



// =========================================
// START
// =========================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        updateNavigation();

    }
);