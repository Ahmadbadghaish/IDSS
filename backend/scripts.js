const express = require('express');
const csvParser = require('csv-parser');
const fs = require('fs');
const fileUpload = require('express-fileupload');
const admin = require('firebase-admin');
const serviceAccount = require('./path-to-your-serviceAccountKey.json');

const app = express();

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: 'https://<YOUR_PROJECT_ID>.firebaseio.com'
});

app.use(express.static('public'));  // Serve static files
app.use(fileUpload());

app.post('/upload', (req, res) => {
    let uploadedFile = req.files.csvFile;
    const filePath = 'temp.csv';
    uploadedFile.mv(filePath, (err) => {
        if (err) return res.status(500).send(err);
        parseCSVAndUploadToFirebase(filePath);
        res.send('Data uploaded to Firebase!');
    });
});

function parseCSVAndUploadToFirebase(filePath) {
    const db = admin.firestore();
    const results = [];
    fs.createReadStream(filePath)
        .pipe(csvParser())
        .on('data', (row) => results.push(row))
        .on('end', () => {
            const batch = db.batch();
            results.forEach(row => {
                const docRef = db.collection('your-collection-name').doc(row.ID);
                batch.set(docRef, row);
            });
            batch.commit();
        });
}

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});
