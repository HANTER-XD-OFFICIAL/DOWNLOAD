// backend/routes/process.js
const express = require('express');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');
const multer = require('multer');
const mockController = require('../controllers/mockController');

const router = express.Router();

// Multer setup for uploads (same as server.js limit)
const uploadDir = path.join(__dirname, '..', '..', 'uploads');
fs.mkdirSync(uploadDir, { recursive: true });

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const safe = Date.now() + '-' + file.originalname.replace(/\s+/g, '_');
    cb(null, safe);
  }
});
const upload = multer({ storage, limits: { fileSize: 200 * 1024 * 1024 } }); // 200MB

// POST /api/process  -- link processor (mock)
router.post('/process', express.json(), mockController.processUrl);

// POST /api/upload  -- file upload and ffmpeg transcode to 1080p
router.post('/upload', upload.single('video'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file uploaded' });

  const uploadsDir = uploadDir;
  const processedDir = path.join(__dirname, '..', '..', 'processed');
  fs.mkdirSync(processedDir, { recursive: true });

  const inputPath = req.file.path;
  const outName = `out-${Date.now()}.mp4`;
  const outPath = path.join(processedDir, outName);

  // ffmpeg -i input -vf "scale=-2:1080" -c:v libx264 -preset fast -crf 23 -c:a aac out.mp4
  const ff = spawn('ffmpeg', ['-y', '-i', inputPath, '-vf', 'scale=-2:1080', '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', '-c:a', 'aac', outPath]);

  ff.stderr.on('data', (d) => console.log('[ffmpeg]', d.toString()));
  ff.on('close', (code) => {
    try { fs.unlinkSync(inputPath); } catch (e) {}
    if (code === 0 && fs.existsSync(outPath)) {
      return res.json({ message: 'Processing complete', download: `/download/${outName}` });
    } else {
      console.error('ffmpeg failed with code', code);
      return res.status(500).json({ error: 'Processing failed' });
    }
  });
});

module.exports = router;