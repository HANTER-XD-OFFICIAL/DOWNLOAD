// Frontend: calls mock backend on /api/process and shows sample download buttons
const btn = document.getElementById('download-btn');
const input = document.getElementById('url-input');
const result = document.getElementById('result');

function sanitize(text){ return String(text).replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

btn.addEventListener('click', async ()=>{
  const url = input.value.trim();
  result.innerHTML = '';
  if(!url){ alert('Please paste a video URL'); return; }
  // show loading
  const p = document.createElement('div'); p.textContent = 'Processing...'; result.appendChild(p);
  try{
    const res = await fetch('/api/process', {
      method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ url })
    });
    if(!res.ok) throw new Error('Server error');
    const data = await res.json();
    // render mock result
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
  }catch(err){
    result.innerHTML = `<div class="error">Error processing URL (mock backend). ${sanitize(err.message)}</div>`;
  }
});

input.addEventListener('keydown', (e)=>{ if(e.key==='Enter') btn.click(); });