// Simple mock server for demo purposes
const express = require('express');
const path = require('path');
const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// POST /api/process -> returns a sample response
app.post('/api/process', (req, res) => {
  const { url } = req.body || {};
  // Very small validation
  if(!url) return res.status(400).json({ error: 'Missing url' });
  // Detect source (very naive)
  let source = 'unknown';
  if(url.includes('tiktok')) source = 'TikTok';
  if(url.includes('youtube') || url.includes('youtu.be')) source = 'YouTube';
  if(url.includes('instagram')) source = 'Instagram';
  if(url.includes('facebook')) source = 'Facebook';

  // Mock response: placeholder links (do NOT point to real content)
  const id = Date.now();
  res.json({
    title: `${source} Sample Video (${id})`,
    source,
    no_watermark: `https://example.com/downloads/${id}-no-watermark.mp4`,
    with_watermark: `https://example.com/downloads/${id}-with-watermark.mp4`,
    audio: `https://example.com/downloads/${id}.mp3`
  });
});

// serve index.html for root
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

const port = process.env.PORT || 3000;
app.listen(port, ()=> console.log('Mock server running on http://localhost:' + port));