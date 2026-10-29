import base64
import streamlit as st

st.set_page_config(page_title="Jailer 2 Generator", page_icon="🎬", layout="centered")

st.title("🎬 Jailer 2 Cinematic Title Card Generator")
st.write("Upload your photo, type your name and initial, and record your video!")

# Sidebar Controls
st.sidebar.header("✨ Customize")
uploaded_file = st.sidebar.file_uploader("Upload Photo", type=["jpg", "png"])
title_name = st.sidebar.text_input("Title Name", "SRINIVASAN N")
initial_letter = st.sidebar.text_input("Initial Letter", "N.S", max_chars=4)
dot_size = st.sidebar.slider("Dot Size", 0.5, 2.0, 1.0, 0.1)

image_url = ""
if uploaded_file is not None:
    b64 = base64.b64encode(uploaded_file.getvalue()).decode()
    image_url = f"data:image/jpeg;base64,{b64}"

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{ margin: 0; background: #000; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
  canvas {{ width: 100% !important; max-width: 900px; height: auto !important; box-shadow: 0 0 20px rgba(255,0,60,0.4); }}
  .btns {{ margin-top: 15px; display: flex; gap: 10px; }}
  button {{ background: #b3002d; color: #fff; border: none; padding: 10px 18px; font-weight: bold; border-radius: 5px; cursor: pointer; }}
  button:hover {{ background: #e60039; }}
  #rec.recording {{ background: #00b33c; }}
</style>
</head>
<body>
  <canvas id="cvs" width="1280" height="720"></canvas>
  <div class="btns">
    <button id="rep">Replay</button>
    <button id="rec">Record & Download WebM</button>
  </div>
<script>
  const canvas = document.getElementById('cvs');
  const ctx = canvas.getContext('2d');
  const titleText = "{title_name}";
  const initSym = "{initial_letter}";
  const dotSize = {dot_size};
  const imgsrc = "{image_url}";

  let dots = [];
  const sCvs = document.createElement('canvas');
  sCvs.width = 180; sCvs.height = 210;
  const sCtx = sCvs.getContext('2d');

  function buildPortrait(img) {{
    sCtx.fillStyle = '#000'; sCtx.fillRect(0, 0, 180, 210);
    sCtx.drawImage(img, 0, 0, 180, 210);
    const data = sCtx.getImageData(0, 0, 180, 210).data;
    dots = [];
    for(let y=0; y<210; y+=2) {{
      for(let x=0; x<180; x+=2) {{
        const idx = (y * 180 + x) * 4;
        const br = (data[idx] * 0.299 + data[idx+1] * 0.587 + data[idx+2] * 0.114);
        if(br > 25) {{
          dots.push({{
            ox: (x - 90) * 2.8,
            oy: (y - 105) * 2.8 - 20,
            br: br,
            phase: Math.random() * Math.PI
          }});
        }}
      }}
    }}
  }}

  const img = new Image();
  img.crossOrigin = "anonymous";
  img.onload = () => buildPortrait(img);
  img.onerror = () => {{
    sCtx.fillStyle = '#000'; sCtx.fillRect(0,0,180,210);
    sCtx.fillStyle = '#fff'; sCtx.beginPath(); sCtx.ellipse(90,80,48,63,0,0,Math.PI*2); sCtx.fill();
    buildPortrait(sCvs);
  }};
  img.src = imgsrc || "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxODAiIGhlaWdodD0iMjEwIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZmZmIi8+PC9zdmc+";

  let start = performance.now();
  const dur = 18000;

  function render(now) {{
    const elapsed = (now - start) % dur;
    const prog = elapsed / dur;

    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, 1280, 720);

    // 1. Star
    if(prog < 0.25) {{
      let p = prog / 0.25;
      ctx.save();
      ctx.translate(640, 360);
      ctx.scale(5 - p * 4, 5 - p * 4);
      ctx.rotate(p * Math.PI * 4);
      ctx.fillStyle = '#fff';
      ctx.beginPath();
      ctx.arc(0, 0, 60, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }}
    // 2. Initial Letter
    else if(prog >= 0.25 && prog < 0.45) {{
      let p = (prog - 0.25) / 0.20;
      ctx.save();
      ctx.font = 'bold 130px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = `rgba(255,255,255,${{p < 0.8 ? p * 3 : (1 - p) * 5}})`;
      ctx.fillText(initSym, 640, 360);
      ctx.restore();
    }}
    // 3 & 4. Portrait Dots
    if(prog >= 0.40) {{
      let p = Math.min(1, (prog - 0.40) / 0.20);
      dots.forEach(d => {{
        let alpha = (d.br / 255) * p;
        ctx.fillStyle = `rgba(255, 180, 210, ${{alpha}})`;
        ctx.fillRect(640 + d.ox, 360 + d.oy, dotSize, dotSize);
      }});
    }}
    // 5. Title Name
    if(prog >= 0.55) {{
      let p = Math.min(1, (prog - 0.55) / 0.25);
      ctx.save();
      ctx.font = '900 42px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = `rgba(255,255,255,${{p}})`;
      ctx.fillText(titleText, 640, 635);
      ctx.restore();
    }}

    requestAnimationFrame(render);
  }}
  requestAnimationFrame(t => {{ start = t; render(t); }});

  document.getElementById('rep').onclick = () => {{ start = performance.now(); }};

  let recorder, chunks = [];
  const recBtn = document.getElementById('rec');
  recBtn.onclick = () => {{
    if(recBtn.classList.contains('recording')) {{
      recorder.stop();
      recBtn.classList.remove('recording');
      recBtn.innerText = "Record & Download WebM";
      return;
    }}
    chunks = [];
    const stream = canvas.captureStream(30);
    recorder = new MediaRecorder(stream, {{ mimeType: 'video/webm' }});
    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = () => {{
      const blob = new Blob(chunks, {{ type: 'video/webm' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'jailer2.webm';
      a.click();
    }};
    start = performance.now();
    recorder.start();
    recBtn.classList.add('recording');
    recBtn.innerText = "Recording... Click to Stop";
    setTimeout(() => {{
      if(recBtn.classList.contains('recording')) {{
        recorder.stop();
        recBtn.classList.remove('recording');
        recBtn.innerText = "Record & Download WebM";
      }}
    }}, dur);
  }};
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=800)
