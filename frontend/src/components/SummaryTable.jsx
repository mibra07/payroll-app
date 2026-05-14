import { useEffect, useState } from "react";
import { getSummary, getCSVUrl } from "../api";

export default function SummaryTable() {

    // --------------------------------------------------------------
    // STEP 1: STATE (DATA STORAGE)
    // --------------------------------------------------------------

    // store API response
    const [data, setData] = useState({ items: []});

    // pagination & offset
    const [limit] = useState(10);
    const [offset, setOffset] = useState(0);
    
    // filter & sorting 
    const [employeeType, setEmployeeType] = useState("");
    const [sort, setSort] = useState("employee_id");
    const [order, setOrder] = useState("asc");

    // UI states
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    // -------------------------------
    // STEP 2: FETCH FUNCTION (API CALL)
    // -------------------------------

    const fetchData = async () => {
        console.log("STEP 2.1 → fetchData() called");

        try {
            setLoading(true);
            setError("");

            const params = {
            limit,
            offset,
            employee_type: employeeType || undefined,
            sort,
            order,
            };

            console.log("STEP 2.2 → Request params:", params);

            // API call
            console.log("STEP 2.3 → Calling getSummary()");
            const res = await getSummary(params);

            console.log("STEP 2.4 → API response:", res.data);

            // save data
            setData(res.data);
            console.log("STEP 2.5 → State updated");

        } catch (err) {
            console.error("STEP 2.ERROR → API failed:", err);

            if (err.response) {
            console.log("STEP 2.ERROR → Server response:", err.response.data);
            setError(err.response.data.detail || "API Error");
            } else {
            setError("Network Error");
            }
        } finally {
            setLoading(false);
            console.log("STEP 2.6 → fetchData finished");
        }
    };
    // -------------------------------
    // STEP 3: useEffect (AUTO RUN)
    // -------------------------------
    useEffect(() => {
    console.log("STEP 3.1 → useEffect triggered");

    fetchData();

    }, [offset, employeeType, sort, order]);

    // -------------------------------
    // STEP 4: HANDLERS (USER ACTIONS)
    // -------------------------------
    const handleEmployeeTypeChange = (e) => {
    console.log("STEP 4.1 → EmployeeType changed:", e.target.value);
    setOffset(0);
    setEmployeeType(e.target.value);
    };

    const handleSortChange = (e) => {
    console.log("STEP 4.2 → Sort changed:", e.target.value);
    setOffset(0);
    setSort(e.target.value);
    };

    const handleOrderChange = (e) => {
    console.log("STEP 4.3 → Order changed:", e.target.value);
    setOffset(0);
    setOrder(e.target.value);
    };

    const handleNext = () => {
    console.log("STEP 4.4 → Next page clicked");
    setOffset(prev => prev + limit);
    };

    const handlePrev = () => {
    console.log("STEP 4.5 → Prev page clicked");
    setOffset(prev => prev - limit);
    };

    // -------------------------------
    // STEP 5: UI (RENDER)
    // -------------------------------
    
    return (
    <div className="card">
        <h3>Summary</h3>

        {/* Filters */}
        <div className="controls">

        {/* Employee Type */}
        <select
            id="employeeType"
            name="employeeType"
            onChange={handleEmployeeTypeChange}
        >
            <option value="">All</option>
            <option value="full-time">Full-time</option>
            <option value="part-time">Part-time</option>
            <option value="contractor">Contractor</option>
        </select>

        {/* Sort */}
        <select
            id="sort"
            name="sort"
            onChange={handleSortChange}
        >
            <option value="employee_id">Employee ID</option>
            <option value="late_hours">Late Hours</option>
            <option value="overtime_hours">Overtime</option>
        </select>

        {/* Order */}
        <select
            id="order"
            name="order"
            onChange={handleOrderChange}
        >
            <option value="asc">ASC</option>
            <option value="desc">DESC</option>
        </select>

        {/* Download CSV */}
        <button
            onClick={() =>
            window.open(
                getCSVUrl({
                employee_type: employeeType,
                sort,
                order,
                })
            )
            }
        >
            Download CSV
        </button>
        </div>

        {/* Loading */}
        {loading && <p className="loading">Loading...</p>}

        {/* Error */}
        {error && <p className="error">{error}</p>}

        {/* Table */}
        {!loading && !error && (
        <table>
            <thead>
            <tr>
                <th>ID</th>
                <th>Late</th>
                <th>Overtime</th>
                <th>Late Cut</th>
                <th>Overtime Pay</th>
            </tr>
            </thead>

            <tbody>
            {!data?.items || data.items.length === 0 ? (
                <tr>
                <td colSpan={5}>No data</td>
                </tr>
            ) : (
                data.items.map((item) => (
                <tr key={item.employee_id}>
                    <td>{item.employee_id}</td>
                    <td>{item.late_hours}</td>
                    <td>{item.overtime_hours}</td>
                    <td>{item.total_late_cut}</td>
                    <td>{item.total_overtime_pay}</td>
                </tr>
                ))
            )}
            </tbody>
        </table>
        )}

        {/* Pagination */}
        <div className="pagination">
        <button
            disabled={offset === 0}
            onClick={handlePrev}
        >
            Prev
        </button>

        <button
            disabled={data.next_offset === null}
            onClick={handleNext}
        >
            Next
        </button>
        </div>
    </div>
    );
}