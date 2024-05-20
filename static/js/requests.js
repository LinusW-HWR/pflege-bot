let currentRequestId = null;

function reloadRequests() {
    fetch('/api', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => updateRequests(data))
    .catch(error => console.error('Error:', error));
}

function updateRequests(data) {
    var requestsDiv = document.querySelector('.requests');
    var currentPath = window.location.pathname;

    requestsDiv.innerHTML = '';

    if (data.length === 0) {
        requestsDiv.innerHTML = `
            <div class="text-center">
                <p>No requests added</p>
            </div>
        `;
    } else {
        data.forEach(request => {
            var statusIndicator = getStatusIndicator(request.status);
            var sendButton = currentPath === '/admin' ? getSendButton(request.id) : '';

            var requestHtml = `
            <div class="bg-secondary p-2 rounded m-3 text-white d-flex justify-content-between hover-effect">
                <div>
                    <div class="d-flex align-items-center">
                        <h2 class="fw-bold fst-italic">${request.name}</h2>
                        ${statusIndicator}
                    </div>
                    <p><span class="fw-bold">Room:</span> <span>${request.room}</span></p>
                    <p><span class="fw-bold">Type:</span> <span>${request.type}</span></p>
                    <p><span class="fw-bold">Medicine:</span> <span>${request.medicine}</span></p>
                </div>
                <div class="d-flex align-items-center">
                    ${sendButton}
                </div>
            </div>
            `;

            requestsDiv.innerHTML += requestHtml;
        });

        document.querySelectorAll(".send-robot").forEach(button => {
            button.addEventListener('click', function() {
                handleSendRobot(button.dataset.requestId);
            });
        });
    }
}

function getStatusIndicator(status) {
    switch (status) {
        case 'pending':
            return `<span class="badge text-bg-warning ms-2">pending</span>`;
        case 'in progress':
            return `<span class="badge text-bg-danger mx-2">in progress</span> <div class="spinner-border text-white" role="status"><span class="sr-only"></span></div>`;
        case 'done':
            return `<span class="badge text-bg-success ms-2">done</span>`;
        default:
            return `<span class="badge text-bg-dark ms-2">unknown</span>`;
    }
}

function getSendButton(requestId) {
    return `<button type="button" class="send-robot btn btn-danger" data-request-id="${requestId}">Send robot</button>`;
}

function handleSendRobot(requestId) {
    fetch(`/api/request?id=${requestId}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        currentRequestId = requestId; // Store the requestId globally
        sendRobot(data["room"]);
        updateRequestStatus(requestId, 'in progress');
    })
    .catch(error => console.error('Error:', error));
}

function sendRobot(room) {
    fetch(`/api/send_robot?room_id=${room}`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(() => {
        var modal = new bootstrap.Modal(document.getElementById('confirmationModal'), {
            keyboard: false
        });
        modal.show();
    })
    .catch(error => console.error('Error:', error));
}

function updateRequestStatus(requestId, status) {
    fetch(`/api/update_req?id=${requestId}&status=${status}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error));
}

function sendHomeYesButtonListener() {
    var modal = bootstrap.Modal.getInstance(document.getElementById('confirmationModal'));
    modal.hide();
    sendHome(currentRequestId); // Pass the currentRequestId
}

function sendHome(requestId) {
    fetch(`/api/send_robot?room_id=0`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(() => updateRequestStatus(requestId, 'done'))
    .catch(error => console.error('Error:', error));
}

function registerSocketEvents() {
    var socket = io();
    socket.on('new_request', function() {
        reloadRequests();
    });
}

function openModalButtonListener() {
    var modal = new bootstrap.Modal(document.getElementById('requestModal'), {
        keyboard: false
    });
    modal.show();
}

function confirmCreateRequestButtonListener() {
    var name = document.getElementById('nameInput').value;
    var room = document.getElementById('roomInput').value;
    var type = document.getElementById('typeInput').value;
    var medicine = document.getElementById('medicineInput').value;

    var request = { name, room, type, medicine };

    fetch('/api/request', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
    })
    .then(response => response.json())
    .then(() => {
        var modal = bootstrap.Modal.getInstance(document.getElementById('requestModal'));
        modal.hide();
        reloadRequests();
    })
    .catch(error => console.error('Error:', error));
}

function requestTypeChangeListener(typeInput, medicineInput) {
    medicineInput.disabled = typeInput.value !== "delivery";
}
