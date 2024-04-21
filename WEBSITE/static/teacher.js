document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('student-results');
    let allStudents = []; // This will hold all the students for filtering

    function normalizeString(str) {
        return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    }

    function fetchAllStudents() {
        fetch('/get_all_students')  // Ensure this URL matches your Flask route
            .then(response => response.json())
            .then(data => {
                allStudents = data; // Save the students in allStudents
                displayStudents(allStudents); // Display all students initially
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function displayStudents(students) {
        resultsContainer.innerHTML = ''; // Clear the container
    
        const table = document.createElement('table');
        table.className = 'table table-striped';
    
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>ID</th>
                <th>Jméno</th>
                <th>Příjmení</th>
                <th>Email</th>
            </tr>`;
        table.appendChild(thead);
    
        const tbody = document.createElement('tbody');
        students.forEach(student => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${student.student_id}</td>
                <td>${student.first_name}</td>
                <td>${student.last_name}</td>
                <td>${student.student_email}</td>
            `;
            tbody.appendChild(tr);
    
            // Add click event to each row
            tr.addEventListener('click', function() {
                window.location.href = `/student_profile/${student.student_id}`; // Redirect to the student's profile page
            });
    
            // Optional: Add a class to cursor to indicate it's clickable
            tr.style.cursor = 'pointer';
        });
    
        table.appendChild(tbody);
        resultsContainer.appendChild(table);
    }

    function filterStudents(query) {
        const normalizedQuery = normalizeString(query);
        const filteredStudents = allStudents.filter(student => {
            return normalizeString(student.first_name + " " + student.last_name).includes(normalizedQuery)
                || normalizeString(student.student_email).includes(normalizedQuery)
                || normalizeString(student.student_id.toString()).includes(normalizedQuery); // Include ID in search
        });
        displayStudents(filteredStudents);
    }

    searchInput.addEventListener('input', function () {
        filterStudents(searchInput.value);
    });

    fetchAllStudents();
});
