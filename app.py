<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jailer 2 Style Title Card - Srinivasan N</title>
    <style>
        body {
            margin: 0;
            background-color: #000;
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
            overflow-x: hidden;
        }
        #canvas-container {
            position: relative;
            width: 1280px;
            height: 720px;
            max-width: 100%;
            box-shadow: 0 0 30px rgba(255, 0, 60, 0.2);
            background: #000;
            margin-top: 10px;
        }
        canvas {
            display: block;
            width: 100%;
            height: 100%;
        }
        .controls-panel {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            background: #111;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 15px 0;
            max-width: 1240px;
            width: 90%;
            border: 1px solid #333;
            box-sizing: border-box;
            align-items: center;
            justify-content: center;
        }
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
            font-size: 13px;
        }
        .control-group label {
            color: #aaa;
        }
        .control-group input[type="text"] {
            background: #222;
            border: 1px solid #444;
            color: #fff;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 14px;
        }
        .control-group input[type="range"] {
            cursor: pointer;
        }
        .btn-container {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
        }
        button {
            background: #b3002d;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 15px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
        }
        button:hover {
            background: #e60039;
            transform: translateY(-1px);
        }
        button:active {
            transform: translateY(1px);
        }
        #record-btn.recording {
            background: #00b33c;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>

    <div id="canvas-container">
        <canvas id="cinemaCanvas" width="1280" height="720"></canvas>
    </div>

    <div class="controls-panel">
        <div class="control-group">
            <label for="nameInput">Title Name:</label>
            <input type="text" id="nameInput" value="SRINIVASAN N">
        </div>
        <div class="control-group">
            <label for="initialInput">Initial Letter:</label>
            <input type="text" id="initialInput" value="N.S" maxlength="4">
        </div>
        <div class="control-group">
            <label for="brightnessSlider">Brightness Cut-off: <span id="brightVal">30</span></label>
            <input type="range" id="brightnessSlider" min="0" max="150" value="30">
        </div>
        <div class="control-group">
            <label for="contrastSlider">Contrast: <span id="contrastVal">1.2</span></label>
            <input type="range" id="contrastSlider" min="0.5" max="2.5" step="0.1" value="1.2">
        </div>
        <div class="control-group">
            <label for="focusSlider">Focus / Dot Size: <span id="focusVal">1.5</span></label>
            <input type="range" id="focusSlider" min="1" max="3" step="0.2" value="1.5">
        </div>
    </div>

    <div class="btn-container">
        <button id="replayBtn">Replay Animation</button>
        <button id="record-btn">Record & Download WebM</button>
    </div>

    <script>
        const canvas = document.getElementById('cinemaCanvas');
        const ctx = canvas.getContext('2d');

        // UI Controls
        const nameInput = document.getElementById('nameInput');
        const initialInput = document.getElementById('initialInput');
        const brightnessSlider = document.getElementById('brightnessSlider');
        const contrastSlider = document.getElementById('contrastSlider');
        const focusSlider = document.getElementById('focusSlider');
        
        document.getElementById('brightVal').innerText = brightnessSlider.value;
        document.getElementById('contrastVal').innerText = contrastSlider.value;
        document.getElementById('focusVal').innerText = focusSlider.value;

        brightnessSlider.oninput = () => document.getElementById('brightVal').innerText = brightnessSlider.value;
        contrastSlider.oninput = () => document.getElementById('contrastVal').innerText = contrastSlider.value;
        focusSlider.oninput = () => document.getElementById('focusVal').innerText = focusSlider.value;

        // Generate Portrait Map
        const sourceCanvas = document.createElement('canvas');
        sourceCanvas.width = 120;
        sourceCanvas.height = 140;
        const sCtx = sourceCanvas.getContext('2d');
        
        function generateSourcePortrait() {
            sCtx.fillStyle = '#000';
            sCtx.fillRect(0, 0, 120, 140);
            
            sCtx.fillStyle = '#fff';
            sCtx.beginPath();
            sCtx.ellipse(60, 55, 32, 42, 0, 0, Math.PI * 2);
            sCtx.fill();
            sCtx.fillRect(30, 15, 60, 25);
            
            sCtx.fillStyle = '#000';
            sCtx.fillRect(45, 45, 10, 6);
            sCtx.fillRect(65, 45, 10, 6);
            sCtx.fillRect(57, 56, 6, 16);
            sCtx.fillRect(48, 80, 24, 8);
        }
        generateSourcePortrait();

        const portraitImgData = sCtx.getImageData(0, 0, 120, 140);
        const portraitDots = [];
        const stepX = 3;
        const stepY = 3;
        for (let y = 0; y < 140; y += stepY) {
            for (let x = 0; x < 120; x += stepX) {
                const idx = (y * 120 + x) * 4;
                const brightness = portraitImgData.data[idx];
                if (brightness > 20) {
                    portraitDots.push({
                        ox: (x - 60) * 4.2,
                        oy: (y - 70) * 4.2 - 20,
                        brightness: brightness,
                        phase: Math.random() * Math.PI * 2,
                        speed: 2 + Math.random() * 3
                    });
                }
            }
        }

        let startTime = performance.now();
        let animationDuration = 18000;

        function draw3DStar(cx, cy, scale, rotAngle) {
            ctx.save();
            ctx.translate(cx, cy);
            ctx.rotate(rotAngle);
            ctx.scale(scale, scale);

            const points = 5;
            const outerR = 120;
            const innerR = 50;

            for (let layer = 0; layer < 3; layer++) {
                const layerScale = 1 - layer * 0.15;
                ctx.beginPath();
                for (let i = 0; i < points * 2; i++) {
                    const r = (i % 2 === 0) ? outerR * layerScale : innerR * layerScale;
                    const angle = (i * Math.PI) / points - Math.PI / 2;
                    const x = Math.cos(angle) * r;
                    const y = Math.sin(angle) * r;
                    if (i === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }
                ctx.closePath();

                const grad = ctx.createLinearGradient(-outerR, -outerR, outerR, outerR);
                if (layer === 0) {
                    grad.addColorStop(0, 'rgba(240, 245, 255, 0.9)');
                    grad.addColorStop(0.5, 'rgba(160, 175, 195, 0.8)');
                    grad.addColorStop(1, 'rgba(90, 100, 115, 0.9)');
                } else if (layer === 1) {
                    grad.addColorStop(0, 'rgba(255, 255, 255, 0.95)');
                    grad.addColorStop(1, 'rgba(120, 135, 150, 0.8)');
                } else {
                    grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
                    grad.addColorStop(1, 'rgba(200, 215, 230, 0.9)');
                }
                ctx.fillStyle = grad;
                ctx.fill();
                ctx.lineWidth = 2 - layer * 0.5;
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
                ctx.stroke();
            }
            ctx.restore();
        }

        const backgroundSparkles = Array.from({ length: 120 }, () => ({
            x: Math.random() * 1280,
            y: Math.random() * 720,
            size: Math.random() * 2 + 0.5,
            alpha: Math.random(),
            twinkleSpeed: 0.02 + Math.random() * 0.05
        }));

        function renderFrame(now) {
            const elapsed = (now - startTime) % animationDuration;
            const progress = elapsed / animationDuration;

            ctx.fillStyle = '#000000';
            ctx.fillRect(0, 0, 1280, 720);

            // Slow Zoom-in effect on whole scene
            const globalZoom = 1.0 + (elapsed / animationDuration) * 0.08;
            ctx.save();
            ctx.translate(640, 360);
            ctx.scale(globalZoom, globalZoom);
            ctx.translate(-640, -360);

            backgroundSparkles.forEach(s => {
                s.alpha += s.twinkleSpeed;
                const currentAlpha = (Math.sin(s.alpha) + 1) / 2 * 0.8;
                ctx.fillStyle = `rgba(255, 255, 255, ${currentAlpha})`;
                ctx.fillRect(s.x, s.y, s.size, s.size);
            });

            // --- STAGE 1: 3D Star ---
            if (progress < 0.25) {
                const sProg = progress / 0.25;
                const starScale = 4.5 - sProg * 3.5;
                const starRot = sProg * Math.PI * 4;
                draw3DStar(640, 360, Math.max(0.01, starScale), starRot);
            } 
            // --- STAGE 2: Initial Letter Formation ---
            else if (progress >= 0.25 && progress < 0.45) {
                const s2Prog = (progress - 0.25) / 0.20;
                
                if (s2Prog < 0.15) {
                    const ballAlpha = 1 - (s2Prog / 0.15);
                    ctx.fillStyle = `rgba(255, 255, 255, ${ballAlpha})`;
                    ctx.beginPath();
                    ctx.arc(640, 360, 8, 0, Math.PI * 2);
                    ctx.fill();
                }

                const currentInitial = initialInput.value || "N.S";
                ctx.save();
                ctx.font = 'bold 130px sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                
                const letterAlpha = s2Prog < 0.8 ? Math.min(1, s2Prog * 3) : Math.max(0, (1 - s2Prog) * 5);
                ctx.shadowColor = 'rgba(255, 0, 80, 0.8)';
                ctx.shadowBlur = 25;
                ctx.fillStyle = `rgba(255, 255, 255, ${letterAlpha})`;
                ctx.fillText(currentInitial, 640, 360);
                ctx.restore();
            }

            // --- STAGE 3 & 4: Dot-Matrix Portrait Build & Twinkle ---
            if (progress >= 0.40) {
                const s3Prog = Math.min(1, (progress - 0.40) / 0.20);
                const cutOff = parseFloat(brightnessSlider.value);
                const contrast = parseFloat(contrastSlider.value);
                const baseDotSize = parseFloat(focusSlider.value);

                if (s3Prog < 1) {
                    ctx.strokeStyle = 'rgba(255, 100, 150, 0.15)';
                    ctx.lineWidth = 1;
                    for (let sx = 400; sx < 880; sx += 15) {
                        ctx.beginPath();
                        ctx.moveTo(sx, 150);
                        ctx.lineTo(sx, 150 + s3Prog * 420);
                        ctx.stroke();
                    }
                }

                portraitDots.forEach((dot) => {
                    const delayNorm = (dot.oy + 70) / 140 * 0.4;
                    const localProg = Math.max(0, Math.min(1, (s3Prog - delayNorm) / 0.6));
                    
                    if (localProg > 0) {
                        let adjustedBright = (dot.brightness - cutOff) * contrast;
                        if (adjustedBright < 0) adjustedBright = 0;
                        const alphaFactor = Math.min(1, adjustedBright / 180) * localProg;

                        dot.phase += 0.05;
                        const twinkle = 0.7 + 0.3 * Math.sin(dot.phase * dot.speed);
                        const finalAlpha = alphaFactor * twinkle;

                        const px = 640 + dot.ox;
                        const py = 360 + dot.oy;

                        ctx.fillStyle = `rgba(255, 180, 210, ${finalAlpha})`;
                        ctx.fillRect(px, py, baseDotSize, baseDotSize);
                    }
                });
            }

            // --- STAGE 5: Title Name Fade-In ---
            if (progress >= 0.55) {
                const s5Prog = Math.min(1, (progress - 0.55) / 0.25);
                const currentName = nameInput.value || "SRINIVASAN N";

                ctx.save();
                ctx.font = '900 42px "Segoe UI", sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                
                ctx.shadowColor = 'rgba(255, 0, 60, 0.9)';
                ctx.shadowBlur = 20;
                ctx.fillStyle = `rgba(255, 255, 255, ${s5Prog})`;
                ctx.fillText(currentName, 640, 635);
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

        // Recording setup (.webm)
        let mediaRecorder;
        let recordedChunks = [];
        const recordBtn = document.getElementById('record-btn');

        recordBtn.onclick = () => {
            if (recordBtn.classList.contains('recording')) {
                mediaRecorder.stop();
                recordBtn.classList.remove('recording');
                recordBtn.innerText = "Record & Download WebM";
                return;
            }

            recordedChunks = [];
            const stream = canvas.captureStream(30);
            try {
                mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm; codecs=vp9' });
            } catch (e) {
                mediaRecorder = new MediaRecorder(stream);
            }

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, { type: 'video/webm' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'jailer2_title_card.webm';
                document.body.appendChild(a);
                a.click();
                setTimeout(() => {
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                }, 100);
            };

            startTime = performance.now();
            mediaRecorder.start();
            recordBtn.classList.add('recording');
            recordBtn.innerText = "Recording... Click to Stop & Save";

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
