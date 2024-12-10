const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');
const app = express();
const fs = require('fs');

const upload = multer({ dest: 'uploads/' });

app.use(express.static('public')); // Serve the frontend files from "public"

// API endpoint to handle image uploads
app.post('/upload', upload.single('image'), (req, res) => {
    const imagePath = req.file.path;

    // Spawn a Python process to handle OCR
    const pythonProcess = spawn('python', ['ocr.py', imagePath]);

    let result = '';
    pythonProcess.stdout.on('data', (data) => {
        result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error('Error:', data.toString());
    });

    pythonProcess.on('close', () => {
        const ocrFilePath = path.join(__dirname, 'uploads', 'ocr_result.txt');
        fs.writeFileSync(ocrFilePath, result);

        // Send the file path to the frontend for downloading
        res.json({ text: result, filePath: `/uploads/ocr_result.txt` });
    });
});


// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
