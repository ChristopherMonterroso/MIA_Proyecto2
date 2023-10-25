const BASE_URL = 'http://127.0.0.1:5000';

export async function CommandToAPI(command, tokens) {
    const url = `${BASE_URL}/commands/${command}`;
    const params = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tokens, confirm })
    };
    return fetch(url, params)
        .then(response => response.json())
        .then(data => data)
        .catch(error => console.error('Error:', error));
}
export async function GetReports() {
    // Realizar la solicitud GET al servidor Flask
    const url = `${BASE_URL}/reports/all`;
    const params = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    };
    
    return fetch(url, params)
        .then(response => response.json())
        .then(data => data)
        .catch(error => console.error('Error:', error));
}