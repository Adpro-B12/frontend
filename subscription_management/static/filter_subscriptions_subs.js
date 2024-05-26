async function filterSubscriptions() {
    let statusFilter = document.getElementById('status').value;
    let apiUrl = '../fetch_subscriptions/';

    console.log("Filtering Subscriptions");
    if(statusFilter) apiUrl += `?status=${statusFilter}`;
    

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => updateSubscriptionCards(data))
        .catch(error => console.error('Error:', error));
}

async function updateSubscriptionCards(subscriptions) {
    const container = document.getElementById('subscription_cards');
    container.innerHTML = ''; // Clear previous content

    let htmlString = '<div class="row row-cols-1 row-cols-md-3 g-4 py-3 justify-content-center">';

    subscriptions.forEach(sub => {
        htmlString += `
        <div class="col mx-5">
            <div class="card">
                <div class="card-header text-center fw-semibold bg-primary text-white">
                    ${sub.uniqueCode}
                </div>
                <div class="card-body text-center">

                    <strong>Status</strong>: ${sub.status} <br>
                    <strong>Start Date</strong>: ${sub.startDate} <br>
                    <strong>End Date</strong>: ${sub.endDate} <br>
                    <strong>ID Box</strong>: ${sub.subscriptionBoxId} <br>
                </div>
                <button class="form-control btn btn-danger fw-bold" onclick="detailToBox(${sub.id})">
                    Cancel
                </button>
            </div>
        </div>
        `;
    });

    htmlString += '</div>';
    container.innerHTML = htmlString;
}

// Example function to handle subscription logic
async function detailToBox(boxId) {
    console.log(`Canceling subscription for box with ID: ${boxId}`);
    window.location.href = `/subscription/cancel/${boxId}/`;
}

filterSubscriptions()
