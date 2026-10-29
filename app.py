import base64
import streamlit as st

st.set_page_config(
    page_title="Jailer 2 Cinematic Title Card Generator",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 Jailer 2 Cinematic Title Card Generator")
st.write(
    "Upload your photo, type your name and initial, and generate your custom"
    " cinematic title card video!"
)

# Sidebar Controls for Users
st.sidebar.header("✨ Customization Controls")
uploaded_file = st.sidebar.file_uploader(
    "Upload Your Photo", type=["jpg", "jpeg", "png"]
)
title_name = st.sidebar.text_input("Title Name", "YOUR NAME")
initial_letter = st.sidebar.text_input(
    "Initial Letter / Symbol", "INITIAL", max_chars=6
)

st.sidebar.subheader("🎛️ Portrait Tuner")
brightness_cutoff = st.sidebar.slider(
    "Brightness Cut-off", min_value=0, max_value=100, value=15
)
contrast_val = st.sidebar.slider(
    "Contrast", min_value=0.5, max_value=3.0, value=1.5, step=0.1
)
dot_size = st.sidebar.slider(
    "Focus / Dot Size", min_value=0.5, max_value=2.0, value=1.0, step=0.1
)

display_title = title_name if title_name else "YOUR NAME"
display_initial = initial_letter if initial_letter else "INITIAL"

image_url = ""
if uploaded_file is not None:
    b64 = base64.b64encode(uploaded_file.getvalue()).decode()
    file_ext = uploaded_file.type.split("/")[-1]
    image_url = f"data:image/{file_ext};base64,{b64}"

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  body {
      margin: 0;
      background-color: #000;
      color: #fff;
      font-family: sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
  }
  #canvas-container {
      position: relative;
      width: 100%;
      max-width: 900px;
      box-shadow: 0 0 25px rgba(255, 0, 60, 0.4);
      background: #000;
  }
  canvas {
      display: block;
      width: 100% !important;
      height: auto !important;
  }
  .btn-container {
      margin-top: 15px;
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: center;
  }
  button, a.download-link {
      background: #b3002d;
      color: white;
      border: none;
      padding: 10px 18px;
      font-size: 14px;
      font-weight: bold;
      border-radius: 5px;
      cursor: pointer;
      text-decoration: none;
      display: inline-block;
      text-align: center;
  }
  button:hover, a.download-link:hover {
      background: #e60039;
  }
  #record-btn.recording {
      background: #00b33c;
  }
  #download-container {
      margin-top: 10px;
  }
</style>
</head>
<body>
  <div id="canvas-container">
      <canvas id="cinemaCanvas" width="1280" height="720"></canvas>
  </div>
  <div class="btn-container">
      <button id="replayBtn">Replay Animation</button>
      <button id="record-btn">Record & Download WebM</button>
  </div>
  <div id="download-container"></div>

<script>
  const canvas = document.getElementById('cinemaCanvas');
  const ctx = canvas.getContext('2d');

  const titleText = "TITLE_PLACEHOLDER";
  const initialSymbol = "INITIAL_PLACEHOLDER";
  const cutOff = CUTOFF_PLACEHOLDER;
  const contrast = CONTRAST_PLACEHOLDER;
  const baseDotSize = FOCUS_PLACEHOLDER;
  const userImgSrc = "IMAGE_PLACEHOLDER";

  let portraitDots = [];
  const sCanvas = document.createElement('canvas');
  sCanvas.width = 240;
  sCanvas.height = 280;
  const sCtx = sCanvas.getContext('2d');

  function buildPortrait(imgObj) {
      sCtx.fillStyle = '#000';
      sCtx.fillRect(0, 0, 240, 280);
      sCtx.drawImage(imgObj, 0, 0, 240, 280);
      const imgData = sCtx.getImageData(0, 0, 240, 280).data;
      portraitDots = [];
      for (let y = 0; y < 280; y += 2) {
          for (let x = 0; x < 240; x += 2) {
              const idx = (y * 240 + x) * 4;
              const r = imgData[idx];
              const g = imgData[idx+1];
              const b = imgData[idx+2];
              const brightness = (r * 0.299 + g * 0.587 + b * 0.114);
              if (brightness > 10) {
                  portraitDots.push({
                      ox: (x - 120) * 2.3,
                      oy: (y - 140) * 2.3 - 20,
                      brightness: brightness,
                      phase: Math.random() * Math.PI * 2,
                      speed: 2 + Math.random() * 3
                  });
              }
          }
      }
  }

  const img = new Image();
  img.crossOrigin = "anonymous";
  img.onload = function() {
      buildPortrait(img);
  };
  img.onerror = function() {
      loadFallbackSilhouette();
  };

  if (userImgSrc !== "") {
      img.src = userImgSrc;
  } else {
      loadFallbackSilhouette();
  }

  function loadFallbackSilhouette() {
      sCtx.fillStyle = '#000';
      sCtx.fillRect(0, 0, 240, 280);
      sCtx.fillStyle = '#fff';
      sCtx.beginPath();
      sCtx.ellipse(120, 110, 60, 80, 0, 0, Math.PI * 2);
      sCtx.fill();
      sCtx.fillRect(60, 30, 120, 50);
      sCtx.fillStyle = '#000';
      sCtx.fillRect(90, 90, 20, 12);
      sCtx.fillRect(130, 90, 20, 12);
      sCtx.fillRect(115, 115, 12, 35);
      sCtx.fillRect(95, 160, 50, 15);
      buildPortrait(sCanvas);
  }

  let startTime = performance.now();
  const animationDuration = 22000;

  function draw3DStar(cx, cy, scale, rotAngle) {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(rotAngle);
      ctx.scale(scale, scale);
      const points = 5, outerR = 120, innerR = 50;

      for (let layer = 0; layer < 3; layer++) {
          const layerScale = 1 - layer * 0.15;
          ctx.beginPath();
          for (let i = 0; i < points * 2; i++) {
              const r = (i % 2 === 0) ? outerR * layerScale : innerR * layerScale;
              const angle = (i * Math.PI) / points - Math.PI / 2;
              const x = Math.cos(angle) * r;
              const y = Math.sin(angle) * r;
              if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
          }
          ctx.closePath();
          const grad = ctx.createLinearGradient(-outerR, -outerR, outerR, outerR);
          grad.addColorStop(0, 'rgba(240, 245, 255, 0.9)');
          grad.addColorStop(1, 'rgba(90, 100, 115, 0.9)');
          ctx.fillStyle = grad;
          ctx.fill();
      }
      ctx.restore();
  }

  const backgroundSparkles = Array.from({ length: 120 }, () => ({
      x: Math.random() * 1280, y: Math.random() * 720,
      size: Math.random() * 2 + 0.5, alpha: Math.random(), twinkleSpeed: 0.03
  }));

  function renderFrame(now) {
      const elapsed = (now - startTime) % animationDuration;
      const progress = elapsed / animationDuration;

      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, 1280, 720);

      const globalZoom = 1.0 + progress * 0.06;
      ctx.save();
      ctx.translate(640, 360);
      ctx.scale(globalZoom, globalZoom);
      ctx.translate(-640, -360);

      backgroundSparkles.forEach(s => {
          s.alpha += s.twinkleSpeed;
          ctx.fillStyle = 'rgba(255, 255, 255, ' + ((Math.sin(s.alpha) + 1) / 2 * 0.7) + ')';
          ctx.fillRect(s.x, s.y, s.size, s.size);
      });

      if (progress < 0.25) {
          const sProg = progress / 0.25;
          draw3DStar(640, 360, Math.max(0.01, 4.5 - sProg * 3.5), sProg * Math.PI * 4);
      }
      else if (progress >= 0.25 && progress < 0.45) {
          const s2Prog = (progress - 0.25) / 0.20;
          ctx.save();
          ctx.font = 'bold 130px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.shadowColor = 'rgba(255, 0, 80, 0.8)';
          ctx.shadowBlur = 25;
          ctx.fillStyle = 'rgba(255, 255, 255, ' + (s2Prog < 0.8 ? s2Prog * 3 : (1 - s2Prog) * 5) + ')';
          ctx.fillText(initialSymbol, 640, 360);
          ctx.restore();
      }

      if (progress >= 0.40) {
          const s3Prog = Math.min(1, (progress - 0.40) / 0.20);
          portraitDots.forEach(dot => {
              const delayNorm = (dot.oy + 140) / 280 * 0.4;
              const localProg = Math.max(0, Math.min(1, (s3Prog - delayNorm) / 0.6));
              if (localProg > 0) {
                  let adj = (dot.brightness - cutOff) * contrast;
                  if (adj < 0) adj = 0;
                  dot.phase += 0.05;
                  const alpha = Math.min(1, adj / 180) * localProg * (0.7 + 0.3 * Math.sin(dot.phase * dot.speed));
                  ctx.fillStyle = 'rgba(255, 180, 210, ' + alpha + ')';
                  ctx.fillRect(640 + dot.ox, 360 + dot.oy, baseDotSize, baseDotSize);
              }
          });
      }

      if (progress >= 0.55) {
          const s5Prog = Math.min(1, (progress - 0.55) / 0.25);
          ctx.save();
          ctx.font = '900 42px sans-serif';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.shadowColor = 'rgba(255, 0, 60, 0.9)';
          ctx.shadowBlur = 20;
          ctx.fillStyle = 'rgba(255, 255, 255, ' + s5Prog + ')';
          ctx.fillText(titleText, 640, 635);
          ctx.restore();
      }

      ctx.restore();
      requestAnimationFrame(renderFrame);
  }

  requestAnimationFrame((now) => {
      startTime = now;
      requestAnimationFrame(renderFrame);
  });

  document.getElementById('replayBtn').onclick = () => {
      startTime = performance.now();
  };

  let mediaRecorder, recordedChunks = [];
  const recordBtn = document.getElementById('record-btn');
  const downloadContainer = document.getElementById('download-container');

  recordBtn.onclick = () => {
      if (recordBtn.classList.contains('recording')) {
          mediaRecorder.stop();
          recordBtn.classList.remove('recording');
          recordBtn.innerText = "Record & Download WebM";
          return;
      }
      recordedChunks = [];
      downloadContainer.innerHTML = "";
      const stream = canvas.captureStream(30);
      try {
          mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm; codecs=vp9' });
      } catch (e) {
          mediaRecorder = new MediaRecorder(stream);
      }

      mediaRecorder.ondataavailable = e => { if (e.data.size > 0) recordedChunks.push(e.data); };
      mediaRecorder.onstop = () => {
          const blob = new Blob(recordedChunks, { type: 'video/webm' });
          const url = URL.createObjectURL(blob);
          downloadContainer.innerHTML = `<a class="download-link" href="${url}" download="jailer2_title.webm">📥 Click Here to Download Your Video (.webm)</a>`;
      };
      startTime = performance.now();
      mediaRecorder.start();
      recordBtn.classList.add('recording');
      recordBtn.innerText = "Recording... Click to Stop";
      setTimeout(() => {
          if (recordBtn.classList.contains('recording')) {
              mediaRecorder.stop();
              recordBtn.classList.remove('recording');
              recordBtn.innerText = "Record & Download WebM";
          }
      }, animationDuration);
  };
</script>
</body>
</html>
"""

html_content = (
    html_template.replace("TITLE_PLACEHOLDER", display_title)
    .replace("INITIAL_PLACEHOLDER", display_initial)
    .replace("CUTOFF_PLACEHOLDER", str(brightness_cutoff))
    .replace("CONTRAST_PLACEHOLDER", str(contrast_val))
    .replace("FOCUS_PLACEHOLDER", str(dot_size))
    .replace("IMAGE_PLACEHOLDER", image_url)
)

st.components.v1.html(html_content, height=850, scrolling=False)
