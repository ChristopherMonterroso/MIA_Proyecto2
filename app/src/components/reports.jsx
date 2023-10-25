import React, { useState, useEffect } from 'react';
import { GetReports } from '../utils/apiRequests';
import './styles/reports.css';
function ReportList() {
  const [reports, setReports] = useState([]);

  const bucket_url = 'https://reportes-command-app.s3.us-east-2.amazonaws.com';
  useEffect(() => {
    // Realizar la solicitud GET al servidor Flask
    fetch('http://127.0.0.1:5000/reports/all')
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (data.error === "false") {
          setReports(data.reports);

        } else {
          console.error('Error al obtener la lista de reportes');
        }
      })
      .catch(error => console.error('Error de red:', error));
  }, []);
  
  return (
    <div className="container-style">
      <h1>Lista de Reportes</h1>
      <ul className="ul-style">
        {reports.map(report => (
          <li key={report} className="li-style">
            <img src={`${bucket_url}/${report}`}  className="img-style" />
            <span className="report-name">{report}</span>
            
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ReportList;
