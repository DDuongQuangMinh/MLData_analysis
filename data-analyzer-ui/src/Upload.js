import React, { useState } from 'react';
import axios from 'axios';

export default function Upload() {
  const [file, setFile] = useState(null);

  const upload = () => {
    const formData = new FormData();
    formData.append('file', file);

    axios.post('http://localhost:8000/api/datasets/', formData, {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    }).then(res => {
      const datasetId = res.data.id;
      window.location = `/eda/${datasetId}`;
    });
  };

  return (
    <div>
      <h2>Upload CSV</h2>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={upload}>Upload</button>
    </div>
  );
}
