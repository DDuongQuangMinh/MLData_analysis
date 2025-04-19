import React, { useState } from 'react';

export default function UploadAndEDA() {
  const [file, setFile] = useState(null);
  const [eda, setEda] = useState(null);

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch('http://localhost:8000/api/upload/', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();

    const edaRes = await fetch(`http://localhost:8000/api/eda/${data.id}/`);
    const edaData = await edaRes.json();
    setEda(edaData);
  };

  return (
    <div>
      <h1>Upload CSV and Analyze</h1>
      <input type="file" accept=".csv" onChange={e => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Upload & Analyze</button>

      {eda && (
        <div>
          <h3>Shape: {eda.shape[0]} rows, {eda.shape[1]} columns</h3>
          <h4>Columns: {eda.columns.join(', ')}</h4>
          <pre>{JSON.stringify(eda.head, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}