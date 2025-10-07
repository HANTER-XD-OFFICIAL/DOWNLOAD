# SSSTik-clone (Frontend + Mock Backend)

This repository is a demo **frontend** (ssstik-style) plus a small **mock backend** for development/testing.

## What you get
- Frontend: `index.html`, `styles.css`, `script.js` — UI that mimics the downloader layout.
- Mock backend: `server.js` (Node/Express) that accepts POST `/api/process` and returns a sample JSON response.
- Use this to test UI workflows. Replace the mock backend with a real implementation when you have legal permission / APIs.

## Run locally (Node.js)
1. Install Node.js (v14+).
2. In the project folder run:
```bash
npm install
node server.js
```
3. Open `http://localhost:3000` in your browser.

## Notes
- This is a development/demo setup. It does not download or remove watermarks from third-party content.
- To enable real downloads you must implement a server-side service that respects platform policies and copyright.