import { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Tooltip,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

function App() {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [selectedFile, setSelectedFile] = useState(null);
  const [currentDataset, setCurrentDataset] = useState(null);
  const [history, setHistory] = useState([]);
  const [status, setStatus] = useState('');

  const authConfig = useMemo(
    () => ({
      auth: {
        username,
        password,
      },
    }),
    [username, password]
  );

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/history/`, authConfig);
      setHistory(response.data);
    } catch (error) {
      setStatus('Unable to fetch history. Check credentials and backend.');
    }
  };

  const fetchLatest = async () => {
    try {
      const response = await axios.get(`${API_URL}/datasets/latest/`, authConfig);
      setCurrentDataset(response.data);
    } catch (error) {
      // ignore if empty
    }
  };

  useEffect(() => {
    fetchHistory();
    fetchLatest();
  }, [authConfig]);

  const handleUpload = async () => {
    if (!selectedFile) {
      setStatus('Select a CSV file before uploading.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setStatus('Uploading...');
    try {
      const response = await axios.post(`${API_URL}/upload/`, formData, {
        ...authConfig,
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setCurrentDataset(response.data);
      setStatus('Upload successful.');
      fetchHistory();
    } catch (error) {
      setStatus(error.response?.data?.error || 'Upload failed.');
    }
  };

  const handleSelectHistory = async (datasetId) => {
    try {
      const response = await axios.get(`${API_URL}/datasets/${datasetId}/`, authConfig);
      setCurrentDataset(response.data);
      setStatus('Loaded dataset.');
    } catch (error) {
      setStatus('Unable to load dataset.');
    }
  };

  const handleDownloadReport = async () => {
    if (!currentDataset?.id) return;
    try {
      const response = await axios.get(`${API_URL}/report/${currentDataset.id}/`, {
        ...authConfig,
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `dataset-report-${currentDataset.id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      setStatus('Failed to download report.');
    }
  };

  const typeChart = useMemo(() => {
    const distribution = currentDataset?.summary?.type_dist || {};
    return {
      labels: Object.keys(distribution),
      datasets: [
        {
          label: 'Equipment Count',
          data: Object.values(distribution),
          backgroundColor: '#4c6ef5',
        },
      ],
    };
  }, [currentDataset]);

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>Chemical Equipment Parameter Visualizer</h1>
          <p>Hybrid Web + Desktop analytics powered by Django & Pandas.</p>
        </div>
        <div className="auth-block">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>
      </header>

      <section className="upload-section">
        <div className="upload-card">
          <h2>Upload CSV</h2>
          <input
            type="file"
            accept=".csv"
            onChange={(event) => setSelectedFile(event.target.files[0])}
          />
          <button onClick={handleUpload}>Upload Dataset</button>
          <p className="status">{status}</p>
        </div>

        <div className="history-card">
          <h2>Recent Uploads</h2>
          <ul>
            {history.map((item) => (
              <li key={item.id}>
                <button onClick={() => handleSelectHistory(item.id)}>
                  {item.name}
                </button>
                <span>{new Date(item.uploaded_at).toLocaleString()}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section className="summary-section">
        <div className="summary-card">
          <h3>Total Records</h3>
          <p>{currentDataset?.summary?.total ?? 0}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Flowrate</h3>
          <p>{currentDataset?.summary?.avg_flow?.toFixed(2) ?? '-'}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Pressure</h3>
          <p>{currentDataset?.summary?.avg_pressure?.toFixed(2) ?? '-'}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Temperature</h3>
          <p>{currentDataset?.summary?.avg_temp?.toFixed(2) ?? '-'}</p>
        </div>
        <button className="report-button" onClick={handleDownloadReport}>
          Download PDF Report
        </button>
      </section>

      <section className="visual-section">
        <div className="chart-card">
          <h2>Equipment Type Distribution</h2>
          {currentDataset ? <Bar data={typeChart} /> : <p>No data</p>}
        </div>
        <div className="table-card">
          <h2>Equipment Table</h2>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  {currentDataset?.columns?.map((col) => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {currentDataset?.data?.map((row, index) => (
                  <tr key={`${row['Equipment Name']}-${index}`}>
                    <td>{row['Equipment Name']}</td>
                    <td>{row.Type}</td>
                    <td>{row.Flowrate}</td>
                    <td>{row.Pressure}</td>
                    <td>{row.Temperature}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
}

export default App;
