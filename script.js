/* frontend/script.js
   Handles UI interactions:
   - POST /api/process for link (mock)
   - POST /api/upload for file upload (real upload->transcode)
*/
const processBtn = document.getElementById('process-btn');
const uploadBtn = document.getElementById('upload-btn');
const input = document.getElementById('url-input');
const fileInput = document.getElementById('file-input');
const result = document.getElementById('result');

function sanitize(t){ return String(t).replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

async function processLink(){
  const url = input.value.trim();
  result.innerHTML = '';
  if(!url){ alert('Please paste a video URL'); return; }
  result.textContent = 'Processing link...';

  try{
    const res = await fetch('/api/process', {
      method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ url })
    });
    if(!res.ok) throw new Error('Server error');
    const data = await res.json();
    renderResult(data);
  }catch(err){
    result.innerHTML = `<div class="card"><strong>Error:</strong> ${sanitize(err.message)}</div>`;
  }
}

function renderResult(data){
  result.innerHTML = `
    <div class="card">
      <p><strong>Title:</strong> ${sanitize(data.title)}</p>
      <p><strong>Source:</strong> ${sanitize(data.source)}</p>
      <div class="buttons">
        <a class="btn-link" href="${sanitize(data.no_watermark)}" target="_blank" rel="noreferrer">Download (No watermark)</a>
        <a class="btn-link" href="${sanitize(data.with_watermark)}" target="_blank" rel="noreferrer">Download (With watermark)</a>
        <a class="btn-link" href="${sanitize(data.audio)}" target="_blank" rel="noreferrer">Extract Audio (MP3)</a>
      </div>
    </div>
  `;
}

async function uploadFile(){
  const file = fileInput.files[0];
  if(!file){ alert('Please select a video file to upload'); return; }
  result.innerHTML = 'Uploading & converting... (may take some time)';
  try{
    const fd = new FormData();
    fd.append('video', file);
    const res = await fetch('/api/upload', { method:'POST', body: fd });
    if(!res.ok) {
      const err = await res.json().catch(()=>({error:'Server error'}));
      throw new Error(err.error || 'Upload failed');
    }
    const data = await res.json();
    result.innerHTML = `<div class="card"><p>${sanitize(data.message)}</p><p><a class="btn-link" href="${sanitize(data.download)}">Download Converted Video</a></p></div>`;
  }catch(err){
    result.innerHTML = `<div class="card"><strong>Error:</strong> ${sanitize(err.message)}</div>`;
  }
}

processBtn.addEventListener('click', processLink);
uploadBtn.addEventListener('click', uploadFile);
input.addEventListener('keydown', (e)=>{ if(e.key==='Enter') processLink(); });