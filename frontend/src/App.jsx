// src/App.jsx

import UploadForm from "./components/UploadForm";
import SummaryTable from "./components/SummaryTable";
import "./styles.css";

function App() {
  return (
    <div>
      <h1>Payroll Dashboard</h1>

      <UploadForm />
      <SummaryTable />
    </div>
  );
}

export default App;