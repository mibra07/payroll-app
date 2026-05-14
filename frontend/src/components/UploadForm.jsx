import { useState } from "react";
import { uploadFile } from "../api";

export default function UploadForm() {
    
    // STEP 1: State init
    const [configFile, setConfigFile] = useState(null);
    const [recordFile, setRecordFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    // STEP 2: File select
    const handleConfigChange = (e) => {
        console.log("STEP 2.1: config file selected");
        const file = e.target.files[0];
        console.log("STEP 2.2: file", file);
        setConfigFile(file);
    }
    const handleRecordChange = (e) => {
        console.log("STEP 2.3: record file selected");
        const file = e.target.files[0];
        console.log("STEP 2.4: file", file);
        setRecordFile(file);
    }

    // STEP 3: Upload trigger
    const handleUpload = async (type) => {
        console.log("STEP 3.1: Upload button click");
        console.log("STEP 3.2: Type", type);
        try {
            // STEP 3.3: Reset state
            setLoading(true);
            setMessage("");
            setError("");
            console.log("STEP 3.3: Loading started");

            // STEP 3.4: Configs upload
            if (type === 'configs') {
                console.log("STEP 3.4: Processing CONFIG upload ");

                if (!configFile) {
                    console.log("STEP 3.4:ERROR no config file");
                    alert("Select config file");
                    return;
                }
                console.log("STEP 3.4: Calling uploadFile()");
                const res = await uploadFile("/configs", configFile);
                console.log("STEP 3.4: Response", res.data);
                setMessage(`Configs uploaded: ${JSON.stringify(res.data)}`);
            }
            // STEP 3.5: Record upload
            else if (type === 'records') {
                console.log("STEP 3.5: Processing RECORDS upload");

                if(!recordFile){
                    console.log("STEP 3.5:ERROR no record file");
                    alert("Select record file");
                    return;
                }
                console.log("STEP 3.5: Calling uploadFile()");
                const res = await uploadFile("/clock-records", recordFile);

                console.log("STEP 3.5: Response", res.data);
                setMessage(`Records uploaded: ${JSON.stringify(res.data)}`);
            }

        } catch (error) {
            console.log("STEP 3:ERROR upload failed", error);
            if(error.response) {
                console.log("STEP 3:ERROR server response", error.response.data);
                setError(error.response.data.detail | "Server error");
            } else {
                setError("Network error");
            }
        } finally {
            // STEP 3.6 finish
            setLoading(false);
            console.log("STEP 3.6 → Upload finished");
        }
    }

    // --------------------------------------------------------------
    // STEP 4: UI
    // --------------------------------------------------------------
    return(
        <div className="card">
            <h3>Upload CSV</h3>
            <div className="controls">
                <input type="file" onChange={handleConfigChange} />
                <button onClick={() => handleUpload('configs')}>Upload Configs</button>
            </div>
            <div className="controls">
                <input type="file" onChange={handleRecordChange} />
                <button onClick={() => handleUpload('records')}>Upload Records</button>
            </div>
            
            {loading && <p className="loading">Uploading...</p>}
            {message && <p className="success">{message}</p>}
            {error && <p className="error">{error}</p>}
        </div>
    );
}