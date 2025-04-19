import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

export default function EDA() {
  const { datasetId } = useParams();
  const [summary, setSummary] = useState({});
  const [visuals, setVisuals] = useState({});

  useEffect(() => {
    axios.get(`http://localhost:8000/api/eda/${datasetId}/`, {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    }).then(res => setSummary(res.data));

    axios.get(`http://localhost:8000/api/eda/${datasetId}/visuals/`, {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    }).then(res => setVisuals(res.data));
  }, [datasetId]);

  return (
    <div>
      <h2>EDA Summary</h2>
      <pre>{JSON.stringify(summary, null, 2)}</pre>

      <h2>Visuals</h2>
      {Object.entries(visuals).map(([col, src]) => (
        <div key={col}>
          <h4>{col}</h4>
          <img src={src} alt={col} width="400" />
        </div>
      ))}

       <button onClick={() => window.location = `/train/${datasetId}`}>Train Model</button>

    </div>
  );
}
