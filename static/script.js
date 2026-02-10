function getLocation() {
    if (!navigator.geolocation) {
        document.getElementById("status").innerText =
            "Geolocation is not supported by your browser.";
        return;
    }

    if (!confirm("Do you allow this app to access your location?")) {
        document.getElementById("status").innerText =
            "Permission denied by user.";
        return;
    }

    document.getElementById("status").innerText =
        "Getting your location...";

    navigator.geolocation.getCurrentPosition(
        sendLocation,
        showError,
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
);
}

function sendLocation(position) {
    fetch("/location", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("status").innerText =
            "Location shared successfully!";
    });
}

function showError() {
    document.getElementById("status").innerText =
        "Unable to retrieve location.";
}