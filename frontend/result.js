function parseCSV(csv_data) {
    const lines = csv_data.trim().split("\n");
    const headers = lines[0].split(',').map(header => header.trim());
    
    // Assuming 'Team_Number' is one of the headers in your CSV.
    const teamIndex = headers.indexOf('Team_Number');
    const desiredHeaders = ['ID', 'major', 'GPA', 'role_in_project'];
    const desiredIndexes = desiredHeaders.map(header => headers.indexOf(header));
  
    // Include the 'Team_Number' index for grouping purposes.
    desiredIndexes.push(teamIndex);
  
    const teamsData = {};
    lines.slice(1).forEach(line => {
      const row = line.split(',').map(cell => cell.trim());
      const teamNumber = row[teamIndex];
      if (!teamsData[teamNumber]) {
        teamsData[teamNumber] = [];
      }
      // Only push the desired data (and 'Team_Number' for the key) to the team's data array.
      teamsData[teamNumber].push(desiredIndexes.map(index => row[index]));
    });
  
  
    return { teamsData, desiredHeaders };
  }
  
  function createTableForTeam(teamData, headers) {
    const table = document.createElement('table');
    const headerRow = document.createElement('tr');
    headers.forEach(header => {
      const headerCell = document.createElement('th');
      headerCell.textContent = header;
      headerRow.appendChild(headerCell);
    });
    table.appendChild(headerRow);
  
    teamData.forEach(row => {
      const dataRow = document.createElement('tr');
      // Exclude the last element which is the 'Team_Number'.
      row.slice(0, -1).forEach(cellData => {
        const cell = document.createElement('td');
        cell.textContent = cellData;
        dataRow.appendChild(cell);
      });
      table.appendChild(dataRow);
    });
  
    return table;
  }
  
  function displayTables(parsedData) {
    const container = document.getElementById('tables-container');
    container.innerHTML = '';
  
    Object.keys(parsedData.teamsData).forEach(teamNumber => {
      const title = document.createElement('h3');
      title.textContent = `Team Number: ${teamNumber}`;
      container.appendChild(title);
  
      const table = createTableForTeam(parsedData.teamsData[teamNumber], parsedData.desiredHeaders);
      container.appendChild(table);
    });
  }
  
  function fetchCSV() {
    fetch('updated_student_data_with_teams.csv')
      .then(response => response.text())
      .then(data => {
        const parsedData = parseCSV(data);
        displayTables(parsedData);
      })
      .catch(error => console.error('Error fetching the CSV:', error));
  }
  
  // Call fetchCSV when the page loads
  fetchCSV();