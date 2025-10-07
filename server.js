// backend/server.js
// Main express app — serves frontend and mounts /api endpoints
const express = require('express');
const path = require('path');
const fs = require('fs');
const processRoutes = require('./routes/process');

const app = express();

// Serve frontend static files
const frontendDir = path.join(__dirname, '..', 'frontend');
app.use(express.static(frontendDir));

// Mount API routes under /api
app.use('/api', processRoutes);

// Serve processed file downloads
const processedDir = path.join(__dirname, '..', 'processed');
fs.mkdirSync(processedDir, { recursive: true });
app.get('/download/:file', (req, res) => {
  const f = path.basename(req.params.file);
  const p = path.join(processedDir, f);
  if (!fs.existsSync(p)) return res.status(404).send('Not found');
  res.download(p, f, (err) => {
    if (err) console.error('Download error', err);
    // optionally: fs.unlinkSync(p) to remove after download
  });
});

// Fallback: serve index.html for client-side routes
app.get('*', (req, res) => {
  res.sendFile(path.join(frontendDir, 'index.html'));
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server running on http://localhost:${port}`));