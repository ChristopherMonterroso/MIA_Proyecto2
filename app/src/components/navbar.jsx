import React from 'react';
import './styles/navbar.css'
function Navbar(props) {
  const handleConsolaClick = (e) => {
    e.preventDefault(); // Evita la acción predeterminada del enlace (navegar a otra página)
    props.onFormSwitch('text_editor'); 
  }
  const handleReportesClick = (e) => {
    e.preventDefault(); // Evita la acción predeterminada del enlace (navegar a otra página)
    props.onFormSwitch('reportList'); 
  }
  return (
    <div className="nav">
      <input type="checkbox" id="nav-check" />
      <div className="nav-header">
        <div className="nav-title">
          Disk manager
        </div>
      </div>
      <div className="nav-btn">
        <label htmlFor="nav-check">
          <span></span>
          <span></span>
          <span></span>
        </label>
      </div>

      <div className="nav-links">
        <a onClick={handleConsolaClick}>Consola</a>
        <a onClick={handleReportesClick}>Reportes</a>
      </div>
    </div>
  );
}

export default Navbar;
