function addOption() {
    const container = document.getElementById('options');
    const count = container.children.length + 1;

    const div = document.createElement('div');
    div.className = 'option';
    div.innerHTML = `
        <input type="text" name="options" placeholder="Option ${count}" required readonly onfocus="this.removeAttribute('readonly')">
        <button type="button" class="delete-btn" onclick="removeOption(this)">✖️</button>
    `;

    container.appendChild(div);
    updatePlaceholders();
}

function removeOption(button) {
    const option = button.closest('.option');
    const options = document.querySelectorAll('.option');
    if (options.length > 2) {
        option.remove();
        updatePlaceholders();
    } else {
        alert('At least two options are required.');
    }
}

function updatePlaceholders() {
    const inputs = document.querySelectorAll('#options input[type="text"]');
    inputs.forEach((input, i) => {
        input.placeholder = `Option ${i + 1}`;
    });
}
