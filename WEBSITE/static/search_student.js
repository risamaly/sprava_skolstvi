document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('student-results');
    let allStudents = []; // This will hold all the students for filtering

    function normalizeString(str) {
        return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    }

    function fetchAllStudents() {
        fetch('/user/get_all_students') // Ensure this matches the correct endpoint in your Flask app
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
        table.className = 'table';
    
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Jméno</th>
                <th>Příjmení</th>
                <th>Rodné číslo</th>
            </tr>`;
        table.appendChild(thead);
    
        const tbody = document.createElement('tbody');
        students.forEach(student => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${student.first_name}</td>
                <td>${student.last_name}</td>
                <td>${student.bcn}</td>
            `;
            if (student.student_id) { // Přidáno pro ověření existence student_id
                tr.addEventListener('click', () => {
                    window.location.href = `/boss/student_profile/${student.student_id}`; // Redirect to student's profile page
                });
                tr.style.cursor = 'pointer';
            }
            tbody.appendChild(tr);
        });
    
        table.appendChild(tbody);
        resultsContainer.appendChild(table);
    }

    function filterStudents(query) {
        const normalizedQuery = normalizeString(query);
        const filteredStudents = allStudents.filter(student => {
            const fullName = normalizeString(student.first_name + " " + student.last_name);
            return fullName.includes(normalizedQuery);
        });
        displayStudents(filteredStudents);
    }

    searchInput.addEventListener('input', function () {
        filterStudents(searchInput.value);
    });

    fetchAllStudents(); // Load initial student data
});
