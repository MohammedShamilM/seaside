// Toggle sidebar visibility
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector('.sidebar');
    const hamburger = document.querySelector('.hamburger');

    hamburger.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    // Optional: Close sidebar when clicking outside on small screens
    document.addEventListener('click', (event) => {
        if (!sidebar.contains(event.target) && !hamburger.contains(event.target) && sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
        }
    });
});

// Initialize Charts
document.addEventListener("DOMContentLoaded", function() {
    // Sales Line Chart using Chart.js
    const salesCtx = document.getElementById("salesChart").getContext("2d");
    new Chart(salesCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [{
                label: 'Sales',
                data: [12000, 19000, 3000, 5000, 20000, 30000, 45000],
                borderColor: '#6a5acd',
                backgroundColor: 'rgba(106, 90, 205, 0.2)',
                borderWidth: 2,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true, position: 'top' }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Pie Chart using D3.js
    const data = [40, 30, 20, 10]; // Dummy data for Sales, Distribution, Returns, and Misc
    const colors = ["#6a5acd", "#ffb347", "#ff6961", "#87ceeb"];
    const pie = d3.pie();
    const arc = d3.arc().innerRadius(0).outerRadius(100);
    const svg = d3.select("#pieChart")
                  .attr("width", 200)
                  .attr("height", 200)
                  .append("g")
                  .attr("transform", "translate(100,100)");

    svg.selectAll("path")
       .data(pie(data))
       .enter()
       .append("path")
       .attr("d", arc)
       .attr("fill", (d, i) => colors[i])
       .attr("stroke", "#ffffff")
       .attr("stroke-width", "2px");

    // Add labels (optional)
    svg.selectAll("text")
       .data(pie(data))
       .enter()
       .append("text")
       .attr("transform", function(d) { return `translate(${arc.centroid(d)})`; })
       .attr("text-anchor", "middle")
       .attr("font-size", "12px")
       .text((d, i) => `${data[i]}%`);
});
// Update JavaScript to handle keyboard events
hamburger.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        sidebar.classList.toggle('open');
    }
});
const sidebarLinks = document.querySelectorAll('.sidebar ul li a');

sidebarLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('open');
        }
    });
});
