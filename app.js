async function getRecommendations() {
    const movieName = document.getElementById("movieInput").value;

    // Clear the recommendations section before loading new results
    const recommendationsDiv = document.getElementById("recommendations");
    recommendationsDiv.innerHTML = "<p>Loading recommendations...</p>";

    try {
        const response = await fetch("http://127.0.0.1:8000/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ movie_name: movieName }),
        });

        const data = await response.json();

        if (response.ok) {
            // Update: Only show movie titles
            recommendationsDiv.innerHTML = data.map(
                (movie) => `<p>🎬 ${movie.title}</p>`
            ).join("");
        } else {
            recommendationsDiv.innerHTML = `<p>${data.error}</p>`;
        }
    } catch (error) {
        console.error("Error fetching recommendations:", error);
        recommendationsDiv.innerHTML = `<p>Failed to fetch recommendations. Check console for details.</p>`;
    }
}
