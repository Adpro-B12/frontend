async function allSubscriptions() {
    let apiUrl = '../get_all_subscriptions/';
    

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
        let codeCell = row.insertCell(0);
        let statusCell = row.insertCell(1);
        let startDateCell = row.insertCell(2);
        let endDateCell = row.insertCell(3);
        let idBoxCell = row.insertCell(4);
        let cancelCell = row.insertCell(5);
        let pendingCell = row.insertCell(6);
        let approveCell = row.insertCell(7);

        codeCell.textContent = box.uniqueCode;
        statusCell.textContent = box.status;
        startDateCell.textContent = box.startDate;
        endDateCell.textContent = box.endDate;
        idBoxCell.textContent = box.subscriptionBoxId;
        
        

        let cancellButton = document.createElement('button');
        cancellButton.textContent = 'Cancel';
        cancellButton.onclick = function() {
            detailToBox(box.id,'cancel'); // Function to handle subscription
        };
        cancelCell.appendChild(cancellButton);

        let pendingButton = document.createElement('button');
        pendingButton.textContent = 'Pending';
        pendingButton.onclick = function() {
            detailToBox(box.id,'pending'); // Function to handle subscription
        };
        pendingCell.appendChild(pendingButton);

        let approveButton = document.createElement('button');
        approveButton.textContent = 'Approve';
        approveButton.onclick = function() {
            detailToBox(box.id,'approve'); // Function to handle subscription
        };
        approveCell.appendChild(approveButton);

    });
}

// Example function to handle subscription logic
async function detailToBox(boxId, status) {
    window.location.href = `/subscription/admins/${status}/${boxId}/`;

}