import base64
import streamlit as st

st.set_page_config(
    page_title="Jailer 2 Style Title Card Generator",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 Jailer 2 Style Cinematic Title Card Generator")
st.write(
    "Upload any photo, type your name and initial, tune the portrait, and"
    " record your custom video!"
)

# Sidebar controls for user customization (left completely blank for any user)
st.sidebar.header("✨ Customize Your Video")

uploaded_file = st.sidebar.file_uploader(
    "Upload Your Photo (JPG/PNG)", type=["jpg", "jpeg", "png"]
)
title_name = st.sidebar.text_input(
    "Title Name", "", placeholder="Enter Name (e.g. RAJINIKANTH)"
)
initial_letter = st.sidebar.text_input(
    "Initial Letter / Symbol", "", max_chars=4, placeholder="e.g. R.K"
)

st.sidebar.subheader("🎛️ Portrait Tuner")
brightness_cutoff = st.sidebar.slider(
    "Brightness Cut-off", min_value=0, max_value=150, value=30
)
contrast_val = st.sidebar.slider(
    "Contrast", min_value=0.5, max_value=2.5, value=1.2, step=0.1
)
focus_size = st.sidebar.slider(
    "Focus / Dot Size", min_value=1.0, max_value=3.0, value=1.5, step=0.2
)

# Fallback text if user leaves inputs empty
display_title = title_name if title_name else "YOUR NAME"
display_initial = initial_letter if initial_letter else "X.Y"

# Convert uploaded image to base64 data URL so JavaScript can read it
image_data_url = ""
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    b64_encoded = base64.b64encode(bytes_data).decode("utf-8")
    file_extension = uploaded_file.type.split("/")[-1]
    image_data_url = f"data:image/{file_extension};base64,{b64_encoded}"

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            background-color: #000;
            color: #fff;
            font-family: sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        #canvas-container {{
            position: relative;
            width: 100%;
            max-width: 900px;
            box-shadow: 0 0 25px rgba(255, 0, 60, 0.4);
            background: #000;
        }}
        canvas {{
            display: block;
            width: 100% !important;
            height: auto !important;
        }}
        .btn-container {{
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }}
        button {{
            background: #b3002d;
            color: white;
            border: none;
            padding: 10px 18px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
        }}
        button:hover {{
            background: #e60039;
        }}
        #record-btn.recording {{
            background: #00b33c;
        }}
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

    <script>
        const canvas = document.getElementById('cinemaCanvas');
        const ctx = canvas.getContext('2d');

        const titleText = "{display_title}";
        const initialSymbol = "{display_initial}";
        const cutOff = {brightness_cutoff};
        const contrast = {contrast_val};
        const baseDotSize = {focus_size};
        const userImgSrc = "{image_data_url}";

        let portraitDots = [];

        const imgObj = new Image();
        imgObj.crossOrigin = "anonymous";
        
        imgObj.onload = function() {{
            extractDotsFromImage(imgObj);
        }};

        imgObj.onerror = function() {{
            loadFallbackSilhouette();
        }};

        if (userImgSrc !== "") {{
            imgObj.src = userImgSrc;
        }} else {{
            loadFallbackSilhouette();
        }}

        function loadFallbackSilhouette() {{
            const sCanvas = document.createElement('canvas');
            sCanvas.width = 120; sCanvas.height = 140;
            const sCtx = sCanvas.getContext('2d');
            sCtx.fillStyle = '#000'; sCtx.fillRect(0, 0, 120, 140);
            sCtx.fillStyle = '#fff';
            sCtx.beginPath(); sCtx.ellipse(60, 55, 32, 42, 0, 0, Math.PI * 2); sCtx.fill();
            sCtx.fillRect(30, 15, 60, 25);
            
            sCtx.fillStyle = '#000';
            sCtx.fillRect(45, 45, 10, 6);
            sCtx.fillRect(65, 45, 10, 6);
            sCtx.fillRect(57, 56, 6, 16);
            sCtx.fillRect(48, 80, 24, 8);
            extractDotsFromImage(sCanvas);
        }}

        function extractDotsFromImage(source) {{
            const sCanvas = document.createElement('canvas');
            sCanvas.width = 120; 
            sCanvas.height = 140;
            const sCtx = sCanvas.getContext('2d');
            sCtx.drawImage(source, 0, 0, 120, 140);
            const imgData = sCtx.getImageData(0, 0, 120, 140);

            portraitDots = [];
            for (let y = 0; y < 140; y += 3) {{
                for (let x = 0; x < 120; x += 3) {{
                    const idx = (y * 120 + x) * 4;
                    const r = imgData.data[idx];
                    const g = imgData.data[idx+1];
                    const b = imgData.data[idx+2];
                    const brightness = (r * 0.299 + g * 0.587 + b * 0.114);
                    if (brightness > 20) {{
                        portraitDots.push({{
                            ox: (x - 60) * 4.2,
                            oy: (y - 70) * 4.2 - 20,
                            brightness: brightness,
                            phase: Math.random() * Math.PI * 2,
                            speed: 2 + Math.random() * 3
                        }});
                    }}
                }}
            }}
        }}

        let startTime = performance.now();
        const animationDuration = 18000;

        function draw3DStar(cx, cy, scale, rotAngle) {{
            ctx.save();
            ctx.translate(cx, cy);
            ctx.rotate(rotAngle);
            ctx.scale(scale, scale);
            const points = 5, outerR = 120, innerR = 50;

            for (let layer = 0; layer < 3; layer++) {{
                const layerScale = 1 - layer * 0.15;
                ctx.beginPath();
                for (let i = 0; i < points * 2; i++) {{
                    const r = (i % 2 === 0) ? outerR * layerScale : innerR * layerScale;
                    const angle = (i * Math.PI) / points - Math.PI / 2;
                    const x = Math.cos(angle) * r;
                    const y = Math.sin(angle) * r;
                    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
                }}
                ctx.closePath();
                const grad = ctx.createLinearGradient(-outerR, -outerR, outerR, outerR);
                grad.addColorStop(0, 'rgba(240, 245, 255, 0.9)');
                grad.addColorStop(1, 'rgba(90, 100, 115, 0.9)');
                ctx.fillStyle = grad;
                ctx.fill();
            }}
            ctx.restore();
        }}

        const backgroundSparkles = Array.from({{ length: 100 }}, () => ({{
            x: Math.random() * 1280, y: Math.random() * 720,
            size: Math.random() * 2 + 0.5, alpha: Math.random(), twinkleSpeed: 0.03
        }}));

        function renderFrame(now) {{
            const elapsed = (now - startTime) % animationDuration;
            const progress = elapsed / animationDuration;

            ctx.fillStyle = '#000000';
            ctx.fillRect(0, 0, 1280, 720);

            backgroundSparkles.forEach(s => {{
                s.alpha += s.twinkleSpeed;
                ctx.fillStyle = 'rgba(255, 255, 255, ' + ((Math.sin(s.alpha) + 1) / 2 * 0.7) + ')';
                ctx.fillRect(s.x, s.y, s.size, s.size);
            }});

            if (progress < 0.25) {{
                const sProg = progress / 0.25;
                draw3DStar(640, 360, Math.max(0.01, 4.5 - sProg * 3.5), sProg * Math.PI * 4);
            }} 
            else if (progress >= 0.25 && progress < 0.45) {{
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
            }}

            if (progress >= 0.40) {{
                const s3Prog = Math.min(1, (progress - 0.40) / 0.20);
                portraitDots.forEach(dot => {{
                    const delayNorm = (dot.oy + 70) / 140 * 0.4;
                    const localProg = Math.max(0, Math.min(1, (s3Prog - delayNorm) / 0.6));
                    if (localProg > 0) {{
                        let adj = (dot.brightness - cutOff) * contrast;
                        if (adj < 0) adj = 0;
                        dot.phase += 0.05;
                        const alpha = Math.min(1, adj / 180) * localProg * (0.7 + 0.3 * Math.sin(dot.phase * dot.speed));
                        ctx.fillStyle = 'rgba(255, 180, 210, ' + alpha + ')';
                        ctx.fillRect(640 + dot.ox, 360 + dot.oy, baseDotSize, baseDotSize);
                    }}
                }});
            }}

            if (progress >= 0.55) {{
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
            }}

            requestAnimationFrame(renderFrame);
        }}

        requestAnimationFrame((now) => {{
            startTime = now;
            requestAnimationFrame(renderFrame);
        }});

        document.getElementById('replayBtn').onclick = () => {{
            startTime = performance.now();
        }};

        let mediaRecorder, recordedChunks = [];
        const recordBtn = document.getElementById('record-btn');
        recordBtn.onclick = () => {{
            if (recordBtn.classList.contains('recording')) {{
                mediaRecorder.stop();
                recordBtn.classList.remove('recording');
                recordBtn.innerText = "Record & Download WebM";
                return;
            }}
            recordedChunks = [];
            const stream = canvas.captureStream(30);
            mediaRecorder = new MediaRecorder(stream, {{ mimeType: 'video/webm' }});
            mediaRecorder.ondataavailable = e => {{ if (e.data.size > 0) recordedChunks.push(e.data); }};
            mediaRecorder.onstop = () => {{
                const blob = new Blob(recordedChunks, {{ type: 'video/webm' }});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url; a.download = 'jailer2_title.webm';
                a.click();
            }};
            startTime = performance.now();
            mediaRecorder.start();
            recordBtn.classList.add('recording');
            recordBtn.innerText = "Recording... Click to Stop";
            setTimeout(() => {{
                if (recordBtn.classList.contains('recording')) {{
                    mediaRecorder.stop();
                    recordBtn.classList.remove('recording');
                    recordBtn.innerText = "Record & Download WebM";
                }}
            }}, animationDuration);
        }};
    </script>
</body>
</html>
"""

st.components.v1.html(html_content, height=800, scrolling=False)
