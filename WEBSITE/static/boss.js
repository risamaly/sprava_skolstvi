document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('employee-results');
    let allEmployees = []; // This will hold all the employees for filtering

    function normalizeString(str) {
        return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    }

    function fetchAllEmployees() {
        fetch('/get_all_employees') // Ensure this URL matches your Flask route
            .then(response => response.json())
            .then(data => {
                allEmployees = data; // Save the employees in allEmployees
                displayEmployees(allEmployees); // Display all employees initially
            })
            .catch(error => {
                console.error('Error fetching employees:', error);
            });
    }

    function displayEmployees(employees) {
        resultsContainer.innerHTML = ''; // Clear the container

        employees.forEach(employee => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${employee.first_name}</td>
                <td>${employee.last_name}</td>
                <td>${employee.email}</td>
                <td>${employee.bcn}</td>
            `;
            resultsContainer.appendChild(tr);
        });
    }

    function filterEmployees(query) {
        const normalizedQuery = normalizeString(query);
        const filteredEmployees = allEmployees.filter(employee => {
            return (
                normalizeString(employee.first_name).includes(normalizedQuery) ||
                normalizeString(employee.last_name).includes(normalizedQuery) ||
                normalizeString(employee.email).includes(normalizedQuery) ||
                normalizeString(employee.bcn.toString()).includes(normalizedQuery)
            );
        });
        displayEmployees(filteredEmployees);
    }

    searchInput.addEventListener('input', function () {
        filterEmployees(searchInput.value);
    });

    fetchAllEmployees();
});
