document.addEventListener("DOMContentLoaded", () => {
    const pollForms = document.querySelectorAll("form.vote-form");

    pollForms.forEach((form) => {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const pollId = form.dataset.pollId;
            const formData = new FormData();

            const inputs = form.querySelectorAll("input[name='choice']");
            inputs.forEach(input => {
                if (input.checked) {
                    formData.append("choice", input.value);
                }
            });

            try {
                const response = await fetch(`/vote/${pollId}`, {
                    method: "POST",
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    updateResults(pollId, data.results);
                } else {
                    alert("Failed to vote.");
                }
            } catch (err) {
                console.error("Error:", err);
            }
        });
    });

    function updateResults(pollId, results) {
        const resultsContainer = document.getElementById(`results-${pollId}`);
        resultsContainer.innerHTML = "";
        results.forEach(opt => {
            const p = document.createElement("p");
            p.innerHTML = `<strong>${opt.text}</strong>: ${opt.votes} votes`;
            resultsContainer.appendChild(p);
        });
    }
});
