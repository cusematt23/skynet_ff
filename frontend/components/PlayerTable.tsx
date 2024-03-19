
'use client';

import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';
import './PlayerTableCSS.css';
import { AgGridReact } from 'ag-grid-react';
import React, { useState, useEffect } from 'react';
//import { useQuery } from 'react-query';
//import 'axios';

const PlayerTable = () => {
  const [rowData, setRowData] = useState([]);
  const [colDefs, setColDefs] = useState([
    { field: 'name', headerClass: 'text-center', cellStyle: { textAlign: 'center' }, filter: true, floatingFilter: true},
    { field: 'salary', headerClass: 'text-center', valueFormatter: (p) => '$' + Math.floor(p.value).toLocaleString(), cellStyle: { textAlign: 'center' }},
    { field: 'projection', headerClass: 'text-center', cellStyle: { textAlign: 'center'}, editable: true},
    { field: 'ownership', headerClass: 'text-center', cellStyle: { textAlign: 'center' }},
    { field: 'ceiling', headerClass: 'text-center', cellStyle: { textAlign: 'center' }},
  ]);

  useEffect(() => {
    const apiUrl = 'http://localhost:8003/slateplayers/9';

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        const extractedData = data.map(player => ({
          name: player.player_name,
          salary: player.salary,
          projection: player.median_proj,
          ownership: player.ownership_proj,
          ceiling: player.ceiling_proj,
        }));
        setRowData(extractedData);
      })
      .catch(error => {
        console.error('Error:', error.message);
      });
  }, []); // Empty dependency array ensures that useEffect runs only once after initial render

  return (
    <div className='flex justify-center'>
    <div style={{ width: '1000px', height: '700px' }}>
      <AgGridReact className="ag-theme-quartz header-test" rowData={rowData} columnDefs={colDefs} />
    </div>
    </div>
  );
};

export default PlayerTable;