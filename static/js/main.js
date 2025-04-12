// Add poll option field
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

// Firework from one origin point
function launchFireworks(x, y) {
    const container = document.getElementById('firework-container');
    for (let i = 0; i < 50; i++) {
        const dot = document.createElement('div');
        dot.className = 'firework';

        const angle = Math.random() * 2 * Math.PI;
        const radius = Math.random() * 180 + 100;

        const offsetX = Math.cos(angle) * radius;
        const offsetY = Math.sin(angle) * radius;

        dot.style.left = `${x}px`;
        dot.style.top = `${y}px`;
        dot.style.setProperty('--x', `${offsetX}px`);
        dot.style.setProperty('--y', `${offsetY}px`);
        dot.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 60%)`;

        container.appendChild(dot);
        setTimeout(() => dot.remove(), 1000);
    }
}

// Launch a big multi-origin burst
function launchFireworksBurst() {
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;

    const offsets = [
        { x: 0, y: 0 },
        { x: -150, y: -100 },
        { x: 150, y: -80 },
        { x: -100, y: 130 },
        { x: 120, y: 110 },
        { x: 0, y: 180 }
    ];

    offsets.forEach(offset => {
        launchFireworks(centerX + offset.x, centerY + offset.y);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.startsWith('/results/')) {
        setTimeout(launchFireworksBurst, 400);
    }
});
