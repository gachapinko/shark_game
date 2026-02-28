import streamlit as st
import base64

st.set_page_config(page_title="ジンベエ・キャッチ", layout="centered")

def get_base64_image(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return ""

shark_base64 = get_base64_image("shark.png")

# タイトル
st.markdown("<h5 style='text-align: center; color: #333; margin-bottom: 0;'>🦈ジンベエザメからの小さな贈り物💩</h5>", unsafe_allow_html=True)

# --- ゲーム画面（縦幅を400pxに縮小） ---
game_html = f"""
<div id="game-container" style="
    height: 400px; 
    width: 100%; 
    background: linear-gradient(#b3e5fc, #0277bd); 
    position: relative; 
    border-radius: 20px; 
    overflow: hidden; 
    touch-action: none;
    border: 4px solid white;
    margin-bottom: 50px; /* ★フッターとの被り防止に余白を追加 */
">
    <div id="overlay" style="
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 100;
    ">
        <div id="message" style="color: white; font-size: 20px; margin-bottom: 20px; font-weight: bold; text-align: center; padding: 0 20px;"></div>
        <button id="start-btn" onclick="handleButtonClick()" style="
            padding: 10px 20px;
            font-size: 18px;
            background: #ffeb3b;
            border: none;
            border-radius: 50px;
            cursor: pointer;
        ">ゲームスタート！</button>
    </div>

    <img id="shark" src="data:image/png;base64,{shark_base64}" style="
        position: absolute; 
        top: 20px; 
        left: 50%; 
        width: 80px; 
        transform: translateX(-50%);
        transition: left 0.8s ease-in-out;
    ">

    <div id="poop" style="position: absolute; top: -60px; left: 50%; font-size: 35px; display: none; z-index: 10;">💩</div>

    <div id="basket" style="
        position: absolute; 
        bottom: 10px; 
        left: 50%; 
        font-size: 50px; 
        transform: translateX(-50%);
        pointer-events: none;
        z-index: 20;
    ">🗑️</div>

    <div id="info-board" style="
        position: absolute; 
        top: 10px; 
        left: 15px; 
        color: white; 
        font-size: 14px; 
        font-weight: bold;
        text-shadow: 1px 1px 2px black;
    ">Lv: 1 | Score: 0</div>
</div>

<script>
    const container = document.getElementById('game-container');
    const shark = document.getElementById('shark');
    const poop = document.getElementById('poop');
    const basket = document.getElementById('basket');
    const infoBoard = document.getElementById('info-board');
    const overlay = document.getElementById('overlay');
    const message = document.getElementById('message');
    const startBtn = document.getElementById('start-btn');

    let basketX = 50;
    let poopY = -60;
    let poopX = 50;
    let sharkX = 50;
    let score = 0;
    let level = 1;
    let poopBaseSpeed = 0.8; 
    let gameActive = false;
    let poopDropping = false;

    function updateInfo() {{
        infoBoard.innerText = `Lv: ${{level}} | Score: ${{score}}`;
    }}

    function handleButtonClick() {{
        if (level > 5) {{
            location.reload();
            return;
        }}
        startGame();
    }}

    function startGame() {{
        overlay.style.display = 'none';
        gameActive = true;
        updateInfo();
        moveShark();
        dropPoopLoop();
        requestAnimationFrame(update);
    }}

    function moveShark() {{
        if(!gameActive) return;
        sharkX = Math.random() * 70 + 15;
        shark.style.left = sharkX + '%';
        shark.style.transform = sharkX > 50 ? 'translateX(-50%) scaleX(-1)' : 'translateX(-50%) scaleX(1)';
        setTimeout(moveShark, Math.max(600, 1800 - (level * 150)));
    }}

    function dropPoopLoop() {{
        if(!gameActive) return;
        if(!poopDropping) {{
            poopX = sharkX; 
            poopY = 20;
            poop.style.display = 'block';
            poopDropping = true;
        }}
        setTimeout(dropPoopLoop, Math.random() * 1500 + 800);
    }}

    function moveBasket(clientX) {{
        const rect = container.getBoundingClientRect();
        const x = ((clientX - rect.left) / rect.width) * 100;
        basketX = Math.max(10, Math.min(90, x));
        basket.style.left = basketX + '%';
    }}
    container.addEventListener('touchmove', (e) => {{
        if(!gameActive) return;
        moveBasket(e.touches[0].clientX);
        e.preventDefault();
    }}, {{ passive: false }});
    container.addEventListener('mousemove', (e) => {{
        if(gameActive) moveBasket(e.clientX);
    }});

    function update() {{
        if(!gameActive) return;

        if(poopDropping) {{
            poopY += poopBaseSpeed + (level * 0.15); 
            
            if (poopY > 75 && poopY < 90) {{
                if (Math.abs(poopX - basketX) < 18) {{
                    score += 1;
                    updateInfo();
                    poopDropping = false;
                    poop.style.display = 'none';
                    if (score > 0 && score % 20 === 0) levelUp();
                }}
            }}
            
            if (poopY > 105) {{
                poopDropping = false;
                poop.style.display = 'none';
            }}
            poop.style.top = poopY + '%';
            poop.style.left = poopX + '%';
        }}
        requestAnimationFrame(update);
    }}

    function levelUp() {{
        gameActive = false;
        level++;
        overlay.style.display = 'flex';
        if (level > 5) {{
            message.innerText = "🎊 ジンベエマスター！ 🎊";
            startBtn.innerText = "もう一度遊ぶ";
        }} else {{
            message.innerText = `🎉 Level ${{level-1}} クリア！`;
            startBtn.innerText = "次のレベルへ進む";
        }}
    }}
</script>
"""

st.components.v1.html(game_html, height=480) # iframeの高さも調整
