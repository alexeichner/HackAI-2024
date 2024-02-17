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
    const command = `python3 ${__dirname}/test.py ${JSON.stringify(formData)}`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return res.status(500).json({ error: 'Internal server error' });
        }

        console.log(`Python script output: ${stdout}`);
        res.json({ result: 'Script executed successfully', output: stdout });
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
