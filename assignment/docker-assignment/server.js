const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch'); // npm install node-fetch@2

const app = express();
const PORT = 3000;

// Serve static files (for HTML, CSS, JS)
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Serve the To-Do HTML form
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/todo.html');
});

// Handle form submission and send to Flask backend
app.post('/submit-todo', async (req, res) => {
    const { itemName, itemDescription } = req.body;

    // Generate UUID and SHA-256 hash on the frontend (optional) or let Flask generate
    const itemUUID = require('crypto').randomUUID();
    const crypto = require('crypto');
    const hash = crypto.createHash('sha256').update(itemName + itemDescription + itemUUID).digest('hex');

    const todoData = {
        itemName,
        itemDescription,
        itemID: 1, // you can generate a counter here if needed
        itemUUID,
        itemHash: hash
    };

    try {
        // Send data to Flask backend
        const response = await fetch('http://127.0.0.1:5000/submittodoitem', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(todoData)
        });

        const result = await response.json();
        res.send(`<h3>${result.message}</h3><a href="/">Go back</a>`);
    } catch (err) {
        console.error(err);
        res.send('Error sending data to Flask backend');
    }
});

app.listen(PORT, () => {
    console.log(`Frontend server running on http://localhost:${PORT}`);
});
