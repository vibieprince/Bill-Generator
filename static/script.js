function addItem() {
    const itemsDiv = document.getElementById('items');
    const newItem = document.createElement('div');
    newItem.classList.add('item');
    newItem.innerHTML = `
        <label>Product Name:</label>
        <input type="text" name="product_name[]" required>
        <label>Quantity:</label>
        <input type="number" name="quantity[]" min="1" required>
        <label>Price:</label>
        <input type="number" name="price[]" min="0.01" step="0.01" required>
    `;
    itemsDiv.appendChild(newItem);
}
