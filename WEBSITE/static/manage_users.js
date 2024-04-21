document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('user-results');
    let allUsers = []; // Uchování všech uživatelů pro filtraci

    function normalizeString(str) {
        if (!str) return ""; // Přidáme kontrolu na prázdné hodnoty
        return str.normalize("NFD")
                  .replace(/[\u0300-\u036f]/g, "")
                  .replace(/\s+/g, "")
                  .toLowerCase();
    }
    
    // Funkce pro načtení všech uživatelů z databáze
    function fetchAllUsers() {
        fetch('/get-all-employees')
            .then(response => response.json())
            .then(data => {
                allUsers = data; // Uložení uživatelů do proměnné
                displayUsers(allUsers); // Zobrazení všech uživatelů
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Funkce pro zobrazení uživatelů v DOM
    function displayUsers(users) {
        resultsContainer.innerHTML = '';
    
        // Vytvoření tabulky pro zobrazení uživatelů
        const table = document.createElement('table');
        table.className = 'table';
    
        // Hlavička tabulky
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Jméno</th>
                <th>Příjmení</th>
                <th>Email</th>
                <th>BCN</th>
                <th>SID</th>
                <th>Role</th>
            </tr>`;
        table.appendChild(thead);
    
        const tbody = document.createElement('tbody');
        users.forEach(user => {
            const tr = document.createElement('tr');
            tr.className = 'user-row'; // Přidáme třídu pro řádky

            tr.innerHTML = `
                <td>${user.first_name || ''}</td>
                <td>${user.last_name || ''}</td>
                <td>${user.user_email || ''}</td>
                <td>${user.bcn || ''}</td> <!-- Přidání BCN -->
                <td>${user.user_sid}</td>
                <td>${user.user_role || ''}</td> <!-- Přidání Role -->
            `;
            const deleteCell = document.createElement('td');
            deleteCell.className = 'delete-cell';
            deleteCell.innerHTML = '<span class="delete-icon">&times;</span>';
            deleteCell.onclick = function () {
                if (confirm(`Opravdu chcete odstranit uživatele s ID ${user.user_sid}?`)) {
                    deleteUser(user.user_sid);
                }
            };

            tr.appendChild(deleteCell); // Přidáme buňku s křížkem na konec řádku
            tbody.appendChild(tr);
        });

        table.appendChild(tbody);
        resultsContainer.appendChild(table);
    }

    function deleteUser(userSid) {
        // Prompt pro zadání důvodu smazání
        const reason = prompt("Prosím, zadejte důvod smazání uživatele:");
        if (reason === null || reason.trim() === "") {
            alert("Musíte zadat důvod smazání.");
            return; // Ukončí funkci, pokud není zadán důvod
        }
    
        // Posílání důvodu spolu s DELETE požadavkem
        fetch(`/delete-user/${userSid}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ reason }) // Posílání důvodu jako části požadavku
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Chyba při odstraňování uživatele.');
            }
            return response.json();
        })
        .then(data => {
            if(data.success) {
                console.log(data.success);
                const userRow = document.getElementById(`user-row-${userSid}`);
                if(userRow) {
                    userRow.remove();
                }
            } else {
                throw new Error(data.error || 'Došlo k chybě při mazání uživatele.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Nelze odstranit uživatele: ' + error.message);
        });
    }

    // Funkce pro filtrování výsledků
    function filterUsers(query) {
        const normalizedQuery = normalizeString(query);
        const filteredUsers = allUsers.filter(user => {
            const normalizedFullName = normalizeString(user.first_name + " " + user.last_name);
            const normalizedEmail = normalizeString(user.user_email);
            const normalizedBcn = user.bcn ? normalizeString(user.bcn.toString()) : '';
            const normalizedSid = normalizeString(user.user_sid.toString());
            const normalizedRole = user.user_role ? normalizeString(user.user_role) : '';
            
            return normalizedFullName.includes(normalizedQuery) ||
                   normalizedEmail.includes(normalizedQuery) ||
                   normalizedBcn.includes(normalizedQuery) ||
                   normalizedSid.includes(normalizedQuery) ||
                   normalizedRole.includes(normalizedQuery);
        });
        displayUsers(filteredUsers);
    }

    // Přidání event listeneru na vyhledávací pole
    searchInput.addEventListener('input', function () {
        filterUsers(searchInput.value);
    });

    // Načtení všech uživatelů při prvním načtení stránky
    fetchAllUsers();
});
