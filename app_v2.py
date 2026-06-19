import streamlit as st
from ultralytics import YOLO
from PIL import Image

# -----------------------------
# Page Setting
# -----------------------------
st.set_page_config(
    page_title="Corrugated Defect Detection",
    page_icon="📦",
    layout="wide"
)

# -----------------------------
# Load Model
# -----------------------------
model = YOLO("best.pt")

# -----------------------------
# Cover / Header
# -----------------------------
st.markdown("""
# 📦 Corrugated Defect Detection System
### ระบบตรวจจับปัญหาแผ่นกระดาษลูกฟูกด้วย AI

ระบบนี้ใช้สำหรับตรวจจับข้อบกพร่องของแผ่นกระดาษลูกฟูก  
โดยโมเดลปัจจุบันสามารถตรวจจับปัญหา **ฟูกล้ม / ลอนล้ม**  
และแสดงสาเหตุพร้อมแนวทางการแก้ไขเบื้องต้น
""")

st.divider()

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Image")
    uploaded_file = st.file_uploader(
        "อัปโหลดรูปภาพแผ่นกระดาษลูกฟูก",
        type=["jpg", "jpeg", "png"]
    )

with col2:
    st.subheader("ℹ️ System Information")
    st.info("""
    - Model: YOLO
    - Confidence: 0.25
    - Current Defect Class: Flute Crush
    - Output: Detection + Cause + Solution
    """)

# -----------------------------
# Defect Information
# -----------------------------
defect_info = {
    "flute-crush": {
        "name": "ฟูกล้ม / ลอนล้ม",
        "symptom": "ลอนกระดาษเสียรูป ยุบ แบน หรือไม่คงรูปตามปกติ ส่งผลต่อความแข็งแรงของแผ่นกระดาษลูกฟูก",
        "cause": """
1. แรงอัดบริเวณ Corrugating Roll ต่ำเกินไป  
2. ความชื้นกระดาษต่ำกว่า 4%  
3. เส้นกาวเกินขอบกระดาษ  
4. กระดาษด้านฟูกหย่อน
""",
        "solution": """
1. เพิ่มแรงอัดบริเวณ Corrugating Roll และตรวจสอบผลผลิต  
2. ลดความเร็วไลน์ให้อยู่ประมาณ 180 m/min  
3. ปรับแรงเบรกให้อยู่ในช่วง 2.0 - 2.5 bar  
4. เปลี่ยนม้วนกระดาษใหม่ และเปิด NCR เพื่อให้ QA ตรวจสอบ  
5. ปรับตำแหน่งเส้นกาวให้อยู่ภายในขอบกระดาษ  
6. ทำความสะอาดลูกลอนด้วยน้ำมัน  
7. เพิ่มการห่อกระดาษด้านฟูกเพื่อให้มีความตึงมากขึ้น  
8. ปรับระดับ Sky Roll ด้านที่กระดาษหย่อนให้สูงขึ้น
"""
    }
}

# -----------------------------
# Prediction
# -----------------------------
if uploaded_file:
    image = Image.open(uploaded_file)

    st.divider()
    st.subheader("🔍 Detection Result")

    results = model.predict(image, conf=0.25)
    result_img = results[0].plot()

    col_img1, col_img2 = st.columns(2)

    with col_img1:
        st.image(image, caption="Original Image", use_container_width=True)

    with col_img2:
        st.image(result_img, caption="Detected Image", use_container_width=True)

    st.divider()

    if len(results[0].boxes) == 0:
        st.success("✅ ไม่พบปัญหา / กระดาษปกติ")
    else:
        st.error("⚠️ พบข้อบกพร่องในแผ่นกระดาษลูกฟูก")

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            info = defect_info.get(class_name)

            if info:
                st.markdown(f"## 🧾 ปัญหาที่พบ: {info['name']}")

                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    st.warning("### อาการ")
                    st.write(info["symptom"])

                with col_b:
                    st.warning("### สาเหตุ")
                    st.write(info["cause"])

                with col_c:
                    st.warning("### วิธีแก้ไข")
                    st.write(info["solution"])

            else:
                st.error(f"พบปัญหา: {class_name}")