const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

// Middleware to parse JSON requests
app.use(bodyParser.json());

// Connect to the existing SQLite database
const db = new sqlite3.Database('../medical_records.db', (err) => {
    if (err) {
        console.error("Error connecting to database:", err.message);
    } else {
        console.log("Connected to SQLite database.");
    }
});

// POST API: Insert patient data
app.post('/add-patient', (req, res) => {
    const { patient_id, patient_name, date, diagnostics } = req.body;

    if (!patient_id || !patient_name || !date || !diagnostics) {
        return res.status(400).json({ error: "All fields are required!" });
    }

    const query = `INSERT INTO patients (patient_id, patient_name, date, diagnostics) VALUES (?, ?, ?, ?)`;

    db.run(query, [patient_id, patient_name, date, diagnostics], function(err) {
        if (err) {
            return res.status(500).json({ error: "Error inserting data", details: err.message });
        }
        res.status(201).json({ message: "Patient added successfully!", patient_id: patient_id });
    });
});

// GET API: Retrieve patient data by patient_id
app.get('/get-patient', (req, res) => {
    const patient_id = req.query.patient_id;

    if (!patient_id) {
        return res.status(400).json({ error: "Patient ID is required!" });
    }

    const query = `SELECT * FROM patients WHERE patient_id = ?`;

    db.get(query, [patient_id], (err, row) => {
        if (err) {
            return res.status(500).json({ error: "Error retrieving data", details: err.message });
        }
        if (!row) {
            return res.status(404).json({ message: "Patient not found!" });
        }
        res.json(row);
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
