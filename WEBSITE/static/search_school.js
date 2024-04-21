document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('school-results'); // Make sure this ID matches your HTML

    function normalizeString(str) {
        return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    }

    function fetchAllSchools() {
        fetch('/user/get_all_schools')  // This matches the Flask route
            .then(response => response.json())
            .then(data => {
                allSchools = data; // Save the schools in allSchools
                displaySchools(allSchools); // Display all schools initially
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function displaySchools(schools) {
        resultsContainer.innerHTML = '';

        const table = document.createElement('table');
        table.className = 'table';

        const thead = document.createElement('thead');
        thead.innerHTML = `<tr><th>Název školy</th><th>Adresa</th></tr>`;
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        schools.forEach(school => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${school.school_name}</td><td>${school.school_adress}</td>`;
            tbody.appendChild(tr);
            tr.addEventListener('click', function() {
                window.location.href = `/school_detail/${school.school_id}`;
            });
            tr.style.cursor = 'pointer';
        });

        table.appendChild(tbody);
        resultsContainer.appendChild(table);
    }

    function filterSchools(query) {
        const normalizedQuery = normalizeString(query);
        const filteredSchools = allSchools.filter(school => {
            const schoolInfo = normalizeString(school.school_name + " " + school.school_adress);
            return schoolInfo.includes(normalizedQuery);
        });
        displaySchools(filteredSchools);
    }

    searchInput.addEventListener('input', function () {
        filterSchools(searchInput.value);
    });

    fetchAllSchools();
});
