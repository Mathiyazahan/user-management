const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Create MySQL connection
const connection = mysql.createConnection({
    host: 'mysql-service', // This should be the service name in OpenShift
    user: 'dbuser',
    password: 'yourpassword',
    database: 'mysqldb'
});

connection.connect();

// Middleware
app.use(bodyParser.json());
app.use(express.static('public'));

// Route to check if user exists
app.get('/api/checkUser/:username', (req, res) => {
    const username = req.params.username;
    connection.query('SELECT * FROM users WHERE username = ?', [username], (error, results) => {
        if (error) {
            return res.status(500).json({ error: 'Database query error' });
        }
        if (results.length > 0) {
            res.json({ exists: true, address: results[0].address });
        } else {
            res.json({ exists: false });
        }
    });
});

// Route to store new user
app.post('/api/storeUser', (req, res) => {
    const { username, address } = req.body;
    connection.query('INSERT INTO users (username, address) VALUES (?, ?)', [username, address], (error, results) => {
        if (error) {
            return res.status(500).json({ success: false, error: 'Database query error' });
        }
        res.json({ success: true });
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
