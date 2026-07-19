import { useState } from "react";
import { FaCloudUploadAlt, FaArrowLeft } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "../styles/upload.css";

function UploadReport() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF file.");
      return;
    }

    try {
      setLoading(true);

      const token = localStorage.getItem("token");

      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post("/reports/upload", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(response.data);

    } catch (error) {
      console.log(error);
      alert("Upload Failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-page">

      <button
        className="back-btn"
        onClick={() => navigate("/dashboard")}
      >
        <FaArrowLeft /> Dashboard
      </button>

      <div className="upload-card">

        <FaCloudUploadAlt className="upload-icon"/>

        <h1>Upload Medical Report</h1>

        <p>
          Upload your laboratory report or medical prescription.
        </p>

        <input
          type="file"
          accept=".pdf"
          onChange={(e)=>setFile(e.target.files[0])}
        />

        {file && (
          <p className="filename">
            📄 {file.name}
          </p>
        )}

        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? "Analyzing with AI..." : "Upload & Analyze"}
        </button>

      </div>

      {result && (
        <div className="result-card">

          <h2>🤖 AI Health Analysis</h2>

          <h3>Summary</h3>
          <p>{result.file.analysis.summary}</p>

          <h3>Abnormal Findings</h3>
          <ul>
            {result.file.analysis.abnormal_findings.map((item,index)=>(
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h3>Health Risks</h3>
          <ul>
            {result.file.analysis.health_risks.map((item,index)=>(
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h3>Recommendations</h3>
          <ul>
            {result.file.analysis.recommendations.map((item,index)=>(
              <li key={index}>{item}</li>
            ))}
          </ul>

          <h3>Doctor Consultation</h3>

          <p>
            <strong>Required:</strong>{" "}
            {result.file.analysis.doctor_consultation.required ? "Yes" : "No"}
          </p>

          <p>
            <strong>Urgency:</strong>{" "}
            {result.file.analysis.doctor_consultation.urgency}
          </p>

          <p>
            <strong>Reason:</strong>{" "}
            {result.file.analysis.doctor_consultation.reason}
          </p>

        </div>
      )}

    </div>
  );
}

export default UploadReport;