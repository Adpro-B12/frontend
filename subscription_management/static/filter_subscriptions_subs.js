async function filterSubscriptions() {
    let name = document.getElementById('status').value;
    let apiUrl = '../fetch_subscriptions/';

    console.log("AKSKKOEKODEO");
    if(name) apiUrl += `?status=${name}`;
    

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => updateTableSubs(data))
        .catch(error => console.error('Error:', error));
}

async function updateTableSubs(boxes) {
    const tableBody = document.getElementById('boxesTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';


    boxes.forEach(box => {
        let row = tableBody.insertRow();
        let nameCell = row.insertCell(0);
        let typeCell = row.insertCell(1);
        let priceCell = row.insertCell(2);
        let detailCell = row.insertCell(3);
        let idBoxCell = row.insertCell(4);
        let cancelCell = row.insertCell(5);


        nameCell.textContent = box.uniqueCode;
        typeCell.textContent = box.status;
        priceCell.textContent = box.startDate;
        detailCell.textContent = box.endDate;
        idBoxCell.textContent = box.subscriptionBoxId;
        

        // Create the subscribe button
        let detailButton = document.createElement('button');
        detailButton.textContent = 'Cancel';
        detailButton.onclick = function() {
            detailToBox(box.id); // Function to handle subscription
        };
        cancelCell.appendChild(detailButton);
    });
}

// Example function to handle subscription logic
async function detailToBox(boxId) {
    console.log(`detaild to box with ID: ${boxId}`);
    window.location.href = `/subscription/cancel/${boxId}/`;
    // Here, you could add more complex logic, such as making a POST request to a server endpoint to handle the subscription.

}