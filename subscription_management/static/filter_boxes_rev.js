async function filterBoxes() {
    let minPrice = document.getElementById('minPrice').value || 0;
    let maxPrice = document.getElementById('maxPrice').value || 100000;
    let name = document.getElementById('name').value;
    let apiUrl = `fetch_boxes/?minPrice=${minPrice}&maxPrice=${maxPrice}`;

    if(name) apiUrl += `&name=${name}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => updateBoxesCards(data))
        .catch(error => console.error('Error:', error));
}

function updateBoxesCards(boxes) {
    const container = document.getElementById('boxesCards');
    container.innerHTML = ''; // Clear previous content

    let htmlString = '<div class="row row-cols-1 row-cols-md-3 g-4 justify-content-center">';

    boxes.forEach(box => {
        htmlString += `
        <div class="col">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">${box.name}</h5>
                    <p class="card-text"><strong>Type:</strong> ${box.type}</p>
                    <p class="card-text"><strong>Price:</strong> ${box.price}</p>
                    <ul class="list-unstyled">
                        ${box.items.map(item => `<li>${item.name} (Quantity: ${item.quantity})</li>`).join('')}
                    </ul>
                </div>
                <div class="card-footer">
                    <button class="btn btn-success" onclick="detailToBox(${box.id})">Detail</button>
                </div>
            </div>
        </div>
        `;
    });

    htmlString += '</div>';
    container.innerHTML = htmlString;
}

async function detailToBox(boxId) {
    console.log(`Navigating to details for box ID: ${boxId}`);
    window.location.href = `/subscription/${boxId}/`;
}

filterBoxes()