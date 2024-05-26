async function allSubscriptions() {
    let apiUrl = '../get_all_subscriptions/';

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => updateSubscriptionsCards(data))
        .catch(error => console.error('Error:', error));
}

function updateSubscriptionsCards(subscriptions) {
    const container = document.getElementById('subscriptionsCards');
    container.innerHTML = '';

    subscriptions.forEach(sub => {
        let card = document.createElement('div');
        card.className = 'col-md-4 mb-4';
        card.innerHTML = `
            <div class="card h-100">
                <div class="card-header">
                    Subscription ID: ${sub.id}
                </div>
                <div class="card-body">
                    <h5 class="card-title">Code: ${sub.uniqueCode}</h5>
                    <p class="card-text">SubscriptionBox ID: ${sub.subscriptionBoxId}</p>
                    <p class="card-text">Status: ${sub.status}</p>
                    <p class="card-text">Start Date: ${sub.startDate}</p>
                    <p class="card-text">End Date: ${sub.endDate}</p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-danger" onclick="detailToBox(${sub.id}, 'cancel')">Cancel</button>
                    <button class="btn btn-warning" onclick="detailToBox(${sub.id}, 'pending')">Pending</button>
                    <button class="btn btn-success" onclick="detailToBox(${sub.id}, 'approve')">Approve</button>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

async function detailToBox(boxId, status) {
    console.log(`Action: ${status} on box with ID: ${boxId}`);
    window.location.href = `/subscription/admins/${status}/${boxId}/`;
}

allSubscriptions()