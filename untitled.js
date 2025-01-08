class City {
    // Constructor to initialize a City object with a name and coordinates (x, y)
    constructor(name, x, y) {
        this.name = name;
        this.x = x;
        this.y = y;
        this.distances = {}; // Object to store distances to other cities
    }

    // Method to set the distance between this city and another city
    setDistance(otherCity, distance) {
        this.distances[otherCity.name] = distance;
    }
}

// Array to store all the cities added by the user
const cities = [];

// Event listener for the "Add City" button
// Adds a new city to the cities array and updates the output
document.getElementById("add-city").addEventListener("click", () => {
    const name = document.getElementById("city-name").value; // Get the city name
    const x = parseFloat(document.getElementById("city-x").value); // Get the x coordinate
    const y = parseFloat(document.getElementById("city-y").value); // Get the y coordinate

    // Ensure all inputs are valid
    if (name && !isNaN(x) && !isNaN(y)) {
        const city = new City(name, x, y); // Create a new City object
        cities.push(city); // Add the city to the array

        // Update the output to show the added city
        const output = document.getElementById("output");
        output.innerHTML += `<p>Added city: ${name} (${x}, ${y})</p>`;
        document.getElementById("city-form").reset(); // Reset the form fields
    } else {
        alert("Please fill in all fields."); // Show an alert if inputs are invalid
    }
});

// Event listener for the "Calculate Optimal Path" button
// Computes distances between cities and displays the path
document.getElementById("calculate-path").addEventListener("click", () => {
    if (cities.length < 2) {
        alert("Add at least two cities."); // Ensure at least two cities are added
        return;
    }

    // Calculate distances between every pair of cities
    for (let i = 0; i < cities.length; i++) {
        for (let j = i + 1; j < cities.length; j++) {
            const distance = Math.sqrt(
                Math.pow(cities[i].x - cities[j].x, 2) +
                Math.pow(cities[i].y - cities[j].y, 2)
            );
            cities[i].setDistance(cities[j], distance); // Set distance for city i
            cities[j].setDistance(cities[i], distance); // Set distance for city j
        }
    }

    // Simplified path calculation logic (just listing city names)
    const path = cities.map(city => city.name).join(" -> ");
    document.getElementById("output").innerHTML = `<p>Path: ${path}</p>`;

    // Call function to draw the path on the canvas
    drawPath();
});

// Function to draw cities and the path connecting them on the canvas
function drawPath() {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas

    // Draw each city as a blue circle
    for (const city of cities) {
        ctx.beginPath();
        ctx.arc(city.x * 5, city.y * 5, 5, 0, 2 * Math.PI); // Scale coordinates for canvas
        ctx.fillStyle = "blue";
        ctx.fill();
        ctx.fillText(city.name, city.x * 5 + 5, city.y * 5 - 5); // Label the city
    }

    // Draw lines connecting the cities to form the path
    ctx.beginPath();
    ctx.strokeStyle = "red";
    ctx.moveTo(cities[0].x * 5, cities[0].y * 5); // Start at the first city
    for (const city of cities) {
        ctx.lineTo(city.x * 5, city.y * 5); // Draw line to the next city
    }
    ctx.lineTo(cities[0].x * 5, cities[0].y * 5); // Close the path by returning to the first city
    ctx.stroke();
}
