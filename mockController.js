// backend/controllers/mockController.js
// Mock link processor: returns sample metadata and placeholder links.
// This is intentionally mock — replace with real integrations / OAuth flows later.
exports.processUrl = (req, res) => {
  const { url } = req.body || {};
  if (!url) return res.status(400).json({ error: 'Missing url' });

  let source = 'Unknown';
  if (url.includes('tiktok')) source = 'TikTok';
  else if (url.includes('youtube') || url.includes('youtu.be')) source = 'YouTube';
  else if (url.includes('instagram')) source = 'Instagram';
  else if (url.includes('facebook')) source = 'Facebook';

  const id = Date.now();
  return res.json({
    title: `${source} Sample Video (${id})`,
    source,
    no_watermark: `https://example.com/downloads/${id}-no-watermark.mp4`,
    with_watermark: `https://example.com/downloads/${id}-with-watermark.mp4`,
    audio: `https://example.com/downloads/${id}.mp3`
  });
};