const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');  // Import the cors middleware

const app = express();
const port = 3000;

app.use(express.json());
app.use(cors());  // Enable CORS for all routes

app.post('/submitData', (req, res) => {
    const formData = req.body;

    // Example command to run a Python script
    const command = `python3 /Users/alexeichner/Documents/GitHub/HackAI-2024/test.py '${JSON.stringify(formData)}'`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            console.error(`Python script stderr: ${stderr}`);
            console.error(`Error executing Python script. Exit code: ${error.code}`);
            return res.status(500).json({ error: 'Internal server error' });
        }

        console.log(`Python script output: ${stdout}`);
        res.json({ result: 'Script executed successfully', output: stdout });
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
