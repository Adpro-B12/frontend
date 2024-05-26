async function filterBoxes() {
    let minPrice = document.getElementById('minPrice').value;
    let maxPrice = document.getElementById('maxPrice').value;
    let name = document.getElementById('name').value;
    let apiUrl = 'fetch_boxes/';


    if(!minPrice) minPrice=0;
    if(!maxPrice) maxPrice=100000;

    apiUrl += `?minPrice=${minPrice}&maxPrice=${maxPrice}`;
    
    if(name) apiUrl += `&name=${name}`;
    

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => updateTable(data))
        .catch(error => console.error('Error:', error));
}

async function updateTable(boxes) {
    const tableBody = document.getElementById('boxesTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';

    boxes.forEach(box => {
        let row = tableBody.insertRow();
        let nameCell = row.insertCell(0);
        let typeCell = row.insertCell(1);
        let priceCell = row.insertCell(2);
        let itemsCell = row.insertCell(3);
        let detailCell = row.insertCell(4); // Cell for the subscribe button

        nameCell.textContent = box.name;
        typeCell.textContent = box.type;
        priceCell.textContent = `$${box.price}`;
        
        let itemList = document.createElement('ul');
        box.items.forEach(item => {
            let li = document.createElement('li');
            li.textContent = `${item.name} (Quantity: ${item.quantity})`;
            itemList.appendChild(li);
        });
        itemsCell.appendChild(itemList);

        // Create the subscribe button
        let detailButton = document.createElement('button');
        detailButton.textContent = 'Detail';
        detailButton.onclick = function() {
            detailToBox(box.id); // Function to handle subscription
        };
        detailCell.appendChild(detailButton);
    });
}

// Example function to handle subscription logic
async function detailToBox(boxId) {
    console.log(`detaild to box with ID: ${boxId}`);
    window.location.href = `/subscription/${boxId}/`;
    // Here, you could add more complex logic, such as making a POST request to a server endpoint to handle the subscription.

}