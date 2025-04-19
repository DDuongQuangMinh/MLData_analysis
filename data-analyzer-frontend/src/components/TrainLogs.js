// src/components/TrainLogs.js
import React, { useEffect, useState } from 'react';

export default function TrainLogs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws/train-logs/');

    socket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setLogs(prev => [...prev, data.log]);
    };

    return () => socket.close();
  }, []);

  return (
    <div>
      <h3>Training Logs</h3>
      <pre>{logs.join('\n')}</pre>
    </div>
  );
}
