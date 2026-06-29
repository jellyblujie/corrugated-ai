import streamlit as st
from ultralytics import YOLO
from PIL import Image
import base64
import html

st.set_page_config(
    page_title="INTER Fiber Corrugator",
    page_icon="📦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

MODEL_PATH = "best.pt"
LOGO_PATH = "logo.png"

@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()

st.markdown("""
<style>
* {
    box-sizing: border-box;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f1fbf5 0%, #f7f8f7 45%, #f7f8f7 100%);
    overflow-x: hidden;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 390px !important;
    width: 100% !important;
    margin: auto !important;
    padding: 22px 16px 36px 16px !important;
    overflow-x: hidden !important;
}

button {
    border-radius: 14px !important;
    font-weight: 800 !important;
}

.stButton > button {
    height: 52px !important;
}

.cover-card {
    margin-top: 150px;
    background: white;
    padding: 38px 22px 34px 22px;
    border-radius: 24px;
    text-align: center;
    box-shadow: 0 12px 35px rgba(16, 168, 74, 0.18);
    border-top: 5px solid #18a84f;
    width: 100%;
}

.cover-logo {
    width: 220px;
    max-width: 100%;
    display: block;
    margin: 0 auto 18px auto;
}

.cover-title {
    color: #0f7a3a;
    font-size: 26px;
    font-weight: 900;
    margin-top: 10px;
    word-break: break-word;
}

.main-title {
    font-size: 24px;
    font-weight: 900;
    color: #111827;
}

.sub {
    color: #7b8790;
    font-size: 14px;
}

.card {
    background: white;
    padding: 17px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.07);
    margin: 14px 0;
    width: 100%;
    overflow-wrap: break-word;
    word-break: break-word;
}

.detail-text {
    line-height: 1.9;
    font-size: 15px;
    color: #111827;
    overflow-wrap: break-word;
    word-break: break-word;
}

.tip-title,
.green-label {
    color: #14984a;
    font-weight: 900;
    font-size: 14px;
    margin-bottom: 8px;
}

.problem-name {
    background: #fff1f1;
    color: #e51b2f;
    border: 1px solid #ffd2d2;
    padding: 14px;
    border-radius: 13px;
    font-weight: 900;
    margin: 20px 0;
    width: 100%;
    overflow-wrap: break-word;
    word-break: break-word;
}

.red-pill {
    display: inline-block;
    background: #fff1f1;
    color: #e51b2f;
    border: 1px solid #ffd2d2;
    padding: 8px 13px;
    border-radius: 999px;
    font-weight: 900;
    font-size: 13px;
}

.confidence {
    color: #9aa3aa;
    font-size: 13px;
    margin-top: 8px;
}

img {
    border-radius: 16px;
    max-width: 100%;
}

hr {
    border: none;
    border-top: 1px solid #e4e8e5;
    margin: 24px 0;
}

.back-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.back-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: white;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 900;
}

.empty-box {
    height: 170px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #9aa3aa;
}
</style>
""", unsafe_allow_html=True)

defect_info = {
    "flute-crush": {
        "name": "ฟูกล้ม / ลอนล้ม",
        "symptom": """ลอนกระดาษเสียรูป ยุบ แบน หรือไม่คงรูปตามปกติ ส่งผลต่อความแข็งแรงของแผ่นกระดาษลูกฟูก""",
        "cause": """1. แรงอัดบริเวณ Corrugating Roll ต่ำเกินไป
2. ความชื้นกระดาษต่ำกว่า 4%
3. เส้นกาวเกินขอบกระดาษ
4. กระดาษด้านฟูกหย่อน""",
        "solution": """1. เพิ่มแรงอัดบริเวณ Corrugating Roll และตรวจสอบผลผลิต
2. ลดความเร็วไลน์ให้อยู่ประมาณ 180 m/min
3. ปรับแรงเบรกให้อยู่ในช่วง 2.0 - 2.5 bar
4. เปลี่ยนม้วนกระดาษใหม่ และเปิด NCR เพื่อให้ QA ตรวจสอบ
5. ปรับตำแหน่งเส้นกาวให้อยู่ภายในขอบกระดาษ
6. ทำความสะอาดลูกลอนด้วยน้ำมัน
7. เพิ่มการห่อกระดาษด้านฟูกเพื่อให้มีความตึงมากขึ้น
8. ปรับระดับ Sky Roll ด้านที่กระดาษหย่อนให้สูงขึ้น""",
        "prevention": """1. ตรวจสอบแรงอัด Corrugating Roll ตามมาตรฐานก่อนเริ่มเดินงาน
2. ควบคุมความชื้นกระดาษให้อยู่ในช่วงที่เหมาะสม
3. ตรวจสอบตำแหน่งเส้นกาวไม่ให้เกินขอบกระดาษ
4. ตรวจสอบความตึงของกระดาษด้านฟูกระหว่างเดินเครื่อง"""
    }
}

if "page" not in st.session_state:
    st.session_state.page = "cover"
if "image_file" not in st.session_state:
    st.session_state.image_file = None
if "result_img" not in st.session_state:
    st.session_state.result_img = None
if "detections" not in st.session_state:
    st.session_state.detections = []

def go(page):
    st.session_state.page = page
    st.rerun()

def reset_scan():
    st.session_state.image_file = None
    st.session_state.result_img = None
    st.session_state.detections = []
    go("scan")

def image_to_base64(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode()

def show_text(text):
    safe_text = html.escape(text).replace("\n", "<br>")
    st.markdown(
        f"<div class='detail-text'>{safe_text}</div>",
        unsafe_allow_html=True
    )

def header(title, subtitle=""):
    if st.button("‹", key=f"back_{title}"):
        if st.session_state.page == "scan":
            go("cover")
        elif st.session_state.page == "result":
            go("scan")
        elif st.session_state.page == "detail":
            go("result")

    st.markdown(f"<div class='main-title'>{title}</div>", unsafe_allow_html=True)

    if subtitle:
        st.markdown(f"<div class='sub'>{subtitle}</div>", unsafe_allow_html=True)

def get_main_detection():
    if len(st.session_state.detections) == 0:
        return None
    return max(st.session_state.detections, key=lambda x: x["confidence"])

def cover_page():
    try:
        logo_base64 = image_to_base64(LOGO_PATH)
        logo_html = f"<img src='data:image/png;base64,{logo_base64}' class='cover-logo'>"
    except Exception:
        logo_html = "<h3>INTER GROUP PACKAGING</h3>"

    st.markdown(
        f"""
        <div class="cover-card">
            {logo_html}
            <div class="cover-title">อินเตอร์ไฟเบอร์คอนเทนเนอร์</div>
            <div class="sub">ระบบ AI ตรวจสอบข้อบกพร่องกระดาษลูกฟูก</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("เริ่มสแกน", use_container_width=True):
        go("scan")

    st.markdown(
        "<p style='text-align:center;color:#78a88b;margin-top:26px;'>🛡️ Powered by AI Vision</p>",
        unsafe_allow_html=True
    )

def scan_page():
    header("สแกนกระดาษ", "อัปโหลดหรือถ่ายภาพเพื่อเริ่มวิเคราะห์")

    st.write("")
    st.write("")

    st.markdown(
        """
        <div class="card">
            <div class="tip-title">ⓘ คำแนะนำ</div>
            ถ่ายภาพแผ่นกระดาษลูกฟูกในแนวตั้ง ให้เห็นพื้นที่ผิวชัดเจน หลีกเลี่ยงเงาและแสงจ้า
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.image_file is not None:
        image_preview = Image.open(st.session_state.image_file).convert("RGB")
        st.image(image_preview, use_container_width=True)
    else:
        st.markdown(
            """
            <div class="card empty-box">
                ยังไม่มีรูปภาพ
            </div>
            """,
            unsafe_allow_html=True
        )

    tab1, tab2 = st.tabs(["📤 อัปโหลด", "📷 ถ่ายภาพ"])

    with tab1:
        uploaded = st.file_uploader(
            "อัปโหลดรูปภาพ",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        if uploaded is not None:
            st.session_state.image_file = uploaded

    with tab2:
        camera = st.camera_input(
            "ถ่ายภาพ",
            label_visibility="collapsed"
        )
        if camera is not None:
            st.session_state.image_file = camera

    if st.button("วิเคราะห์", use_container_width=True):
        if st.session_state.image_file is None:
            st.warning("กรุณาอัปโหลดหรือถ่ายภาพก่อนวิเคราะห์")
        else:
            with st.spinner("กำลังวิเคราะห์ภาพ..."):
                image = Image.open(st.session_state.image_file).convert("RGB")
                results = model.predict(image, conf=0.25)

                st.session_state.result_img = results[0].plot()

                detections = []
                for box in results[0].boxes:
                    cls_id = int(box.cls[0])
                    class_name = model.names[cls_id]
                    confidence = float(box.conf[0]) * 100
                    detections.append({
                        "class_name": class_name,
                        "confidence": confidence
                    })

                st.session_state.detections = detections
                go("result")

def result_page():
    header("ผลการตรวจสอบ")

    st.write("")

    if st.session_state.result_img is not None:
        st.image(st.session_state.result_img, use_container_width=True)

    detection = get_main_detection()

    if detection is None:
        st.success("✅ ไม่พบข้อบกพร่อง")
        if st.button("สแกนใหม่", use_container_width=True):
            reset_scan()
        return

    class_name = detection["class_name"]
    confidence = detection["confidence"]
    info = defect_info.get(class_name)

    st.markdown(
        f"""
        <div class="card">
            <span class="red-pill">ⓘ พบข้อบกพร่อง</span>
            <div class="confidence">ความมั่นใจ {confidence:.0f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='green-label'>ชื่อปัญหา</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='detail-text'><b>{info['name'] if info else class_name}</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if info is not None:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='green-label'>อาการ</div>", unsafe_allow_html=True)
        show_text(info["symptom"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='green-label'>สาเหตุ</div>", unsafe_allow_html=True)
        show_text(info["cause"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='green-label'>วิธีแก้ไข</div>", unsafe_allow_html=True)
        show_text(info["solution"])
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("ดูรายละเอียด", use_container_width=True):
        go("detail")

    if st.button("สแกนใหม่", use_container_width=True):
        reset_scan()

def detail_page():
    header("รายละเอียดปัญหา")

    detection = get_main_detection()

    if detection is None:
        st.warning("ยังไม่มีผลการตรวจสอบ")
        return

    class_name = detection["class_name"]
    info = defect_info.get(class_name)

    if info is None:
        st.error(class_name)
        return

    st.markdown(f"<div class='problem-name'>{info['name']}</div>", unsafe_allow_html=True)

    st.markdown("<div class='green-label'>อาการ</div>", unsafe_allow_html=True)
    show_text(info["symptom"])

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<div class='green-label'>สาเหตุของปัญหา</div>", unsafe_allow_html=True)
    show_text(info["cause"])

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<div class='green-label'>วิธีการแก้ไข</div>", unsafe_allow_html=True)
    show_text(info["solution"])

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<div class='green-label'>การป้องกัน</div>", unsafe_allow_html=True)
    show_text(info["prevention"])

    st.write("")

    if st.button("กลับไปหน้าผลลัพธ์", use_container_width=True):
        go("result")

if st.session_state.page == "cover":
    cover_page()
elif st.session_state.page == "scan":
    scan_page()
elif st.session_state.page == "result":
    result_page()
elif st.session_state.page == "detail":
    detail_page()