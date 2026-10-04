import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import requests
import os
import av
import time
from dotenv import load_dotenv
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration

from services.yolo_service import load_model, detect
from services.llm_service import get_llm_solution, parse_llm_response
from services.disease_service import get_disease_info
from simulation.simulation_data import FIELD, DRONE, ZONES, INSPECTIONS
from components.ui import inject_css, metric_card, severity_badge, status_badge, section_title

load_dotenv()
st.set_page_config(page_title="CropGuard", page_icon="🌱", layout="wide")
inject_css()

model = load_model()

if "role" not in st.session_state:
    st.session_state.role = "Farmer"
if "llm" not in st.session_state:
    st.session_state.llm = ""
if "last_labels" not in st.session_state:
    st.session_state.last_labels = []
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "B3"
if "spray_status" not in st.session_state:
    st.session_state.spray_status = "Ready"

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        '<div class="brand"><span>🌱</span><div><b>CropGuard</b><small>Precision Agriculture</small></div></div>',
        unsafe_allow_html=True,
    )

    st.session_state.role = st.radio(
        "Role",
        ["Farmer", "Controller"],
        index=0 if st.session_state.role == "Farmer" else 1,
        horizontal=True,
    )

    st.divider()

    if st.session_state.role == "Farmer":
        page = st.radio(
            "Farmer",
            ["Field Overview", "Disease Detection", "Severity Map", "Learn & Prevent", "Inspection History"],
            #label_visibility="collapsed",
        )
    else:
        page = st.radio(
            "Controller",
            ["Drone Control", "Live Mission", "Detection Monitor", "Inspection History"],
            #label_visibility="collapsed",
        )

    st.divider()
    st.caption("Competition prototype")
    st.caption("Drone telemetry, GPS, field map and spraying are simulated.")

# ============================================================
# FARMER
# ============================================================
def render_field_map():
    import plotly.graph_objects as go

    colors = {"High": "#ef4444", "Medium": "#eab308", "Low": "#3b82f6"}
    fig = go.Figure()

    for r in range(4):
        for c in range(6):
            zone_id = f"{chr(65+r)}{c+1}"
            zone = next(z for z in ZONES if z["id"] == zone_id)
            fig.add_trace(go.Scatter(
                x=[c], y=[3-r],
                mode="markers+text",
                text=[zone_id],
                textposition="middle center",
                marker=dict(
                    size=58,
                    color=colors[zone["severity"]],
                    line=dict(width=2, color="white"),
                ),
                customdata=[[zone_id]],
                hovertemplate=(
                    f"<b>{zone_id}</b><br>"
                    f"Severity: {zone['severity']}<br>"
                    f"Affected area: {zone['affected_area']}%<extra></extra>"
                ),
                showlegend=False,
            ))

    fig.update_layout(
        height=430,
        margin=dict(l=5, r=5, t=5, b=5),
        xaxis=dict(visible=False, range=[-0.6, 5.6]),
        yaxis=dict(visible=False, range=[-0.6, 3.6]),
        plot_bgcolor="#f7faf7",
        paper_bgcolor="white",
        dragmode=False,
    )

    event = st.plotly_chart(
        fig,
        use_container_width=True,
        on_select="rerun",
        key="severity_map",
    )

    if event and getattr(event, "selection", None):
        points = event.selection.points
        if points:
            selected = points[0].get("customdata")
            if selected:
                st.session_state.selected_zone = selected[0]
                st.rerun()

    cols = st.columns(3)
    for col, label in zip(cols, ["Low", "Medium", "High"]):
        with col:
            st.markdown(
                f'<div class="legend-item"><span class="dot {label.lower()}"></span>{label}</div>',
                unsafe_allow_html=True,
            )


def farmer_dashboard():
    if page == "Field Overview":
        st.markdown("## Field Overview")
        st.caption("How healthy is the field, where is the problem, and what should be done?")

        cols = st.columns(4)
        cards = [
            ("Field Health", f"{FIELD['health']}%", "Healthy crop coverage"),
            ("Affected Zones", FIELD["affected_zones"], "Zones needing attention"),
            ("Diseases", FIELD["diseases"], "Detected in latest inspection"),
            ("Inspected", FIELD["plants_inspected"], "Plants / areas inspected"),
        ]
        for col, data in zip(cols, cards):
            with col:
                metric_card(*data)

        st.markdown("")
        left, right = st.columns([1.3, 0.7])

        with left:
            section_title("Field Severity Map", "Red = high · Yellow = medium · Blue = low")
            render_field_map()

        with right:
            section_title("Latest Disease", "The important information first.")
            st.markdown(
                f"""
                <div class="disease-card">
                    <div class="eyebrow">DISEASE DETECTED</div>
                    <h2>{FIELD["disease"]}</h2>
                    <p>Your corn plants show signs of <b>{FIELD["disease"]}</b>.</p>
                    <div class="mini-grid">
                        <div><span>Confidence</span><strong>{FIELD["confidence"]}%</strong></div>
                        <div><span>Severity</span><strong>{FIELD["severity"]}</strong></div>
                        <div><span>Field</span><strong>{FIELD["name"]}</strong></div>
                        <div><span>Last inspection</span><strong>10:42 AM</strong></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            info = get_disease_info(FIELD["disease"])
            st.markdown("**What is it?**")
            st.write(info["what"])
            st.markdown("**What should I do?**")
            st.write(info["action"])

    elif page == "Disease Detection":
        st.markdown("## Disease Detection")
        st.caption("AI results translated into farmer-friendly information.")

        info = get_disease_info(FIELD["disease"])

        st.markdown(
            f"""
            <div class="hero-disease">
                <div>
                    <div class="eyebrow">YOUR CROP SHOWS SIGNS OF</div>
                    <h1>{FIELD["disease"]}</h1>
                    <p>Detection confidence: <b>{FIELD["confidence"]}%</b> · Current severity: <b>{FIELD["severity"]}</b></p>
                </div>
                <div>{severity_badge(FIELD["severity"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        a, b = st.columns(2)
        with a:
            st.markdown("### What is it?")
            st.write(info["what"])
            st.markdown("### Common symptoms")
            for x in info["symptoms"]:
                st.markdown(f"- {x}")
            st.markdown("### What causes it?")
            st.write(info["cause"])

        with b:
            st.markdown("### What should I do?")
            st.write(info["action"])
            st.markdown("### How can I prevent it?")
            for x in info["prevention"]:
                st.markdown(f"- {x}")
            st.info(f"Recommended next inspection: {info['reinspect']}")

    elif page == "Severity Map":
        st.markdown("## Field Severity Map")
        st.caption("Select a zone to inspect its disease and intervention information.")
        render_field_map()

        zone = next(z for z in ZONES if z["id"] == st.session_state.selected_zone)
        st.markdown(
            f"""
            <div class="zone-detail">
                <div class="eyebrow">SELECTED ZONE</div>
                <h2>{zone["id"]} {severity_badge(zone["severity"])}</h2>
                <div class="detail-grid">
                    <div><span>Disease</span><b>{zone["disease"]}</b></div>
                    <div><span>Affected area</span><b>{zone["affected_area"]}%</b></div>
                    <div><span>Affected plants</span><b>{zone["affected_plants"]}</b></div>
                    <div><span>Recommendation</span><b>{zone["recommendation"]}</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif page == "Learn & Prevent":
        st.markdown("## Learn About Your Crop")
        info = get_disease_info(FIELD["disease"])

        for title, body in [
            ("What is this disease?", info["what"]),
            ("What causes it?", info["cause"]),
            ("Common symptoms", "\n".join(f"• {x}" for x in info["symptoms"])),
            ("How it spreads", info["spread"]),
            ("What conditions encourage it?", info["conditions"]),
            ("What can the farmer do?", info["action"]),
            ("Preventive practices", "\n".join(f"• {x}" for x in info["prevention"])),
            ("When should I inspect again?", info["reinspect"]),
        ]:
            with st.expander(title, expanded=title in ["What is this disease?", "What can the farmer do?"]):
                st.write(body)

    elif page == "Inspection History":
        st.markdown("## Inspection History")
        st.caption("Historical data is simulated for the prototype.")
        st.dataframe(INSPECTIONS, use_container_width=True, hide_index=True)

# ============================================================
# CONTROLLER
# ============================================================
def render_drone_map():
    import plotly.graph_objects as go

    path = DRONE["path"]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[p[0] for p in path],
        y=[p[1] for p in path],
        mode="lines+markers",
        line=dict(width=3),
        name="Inspection path",
    ))

    fig.add_trace(go.Scatter(
        x=[DRONE["position"][0]],
        y=[DRONE["position"][1]],
        mode="markers+text",
        text=["DRONE"],
        textposition="top center",
        marker=dict(size=18, symbol="triangle-up"),
        name="Drone",
    ))

    for z in ZONES:
        if z["severity"] == "High":
            fig.add_trace(go.Scatter(
                x=[z["map_x"]], y=[z["map_y"]],
                mode="markers",
                marker=dict(size=16, symbol="x"),
                name=f"Hotspot {z['id']}",
            ))

    fig.update_layout(
        height=450,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Field X",
        yaxis_title="Field Y",
        plot_bgcolor="#f7faf7",
        paper_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)


class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.prev = time.time()
        self.fps = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        now = time.time()
        dt = max(now - self.prev, 1e-6)
        self.fps = 0.9 * self.fps + 0.1 * (1 / dt)
        self.prev = now

        img, labels = detect(img)

        # Keep the original application's useful state behavior.
        # We do not make the Streamlit UI update from the worker thread.
        if labels:
            current = labels[0]
            if current != getattr(self, "last_label", None):
                self.last_label = current

        img = draw_hud(img, self.fps, labels, drone_mode=True)
        return av.VideoFrame.from_ndarray(img, format="bgr24")


def draw_hud(frame, fps, labels, drone_mode=False):
    count = len(labels)
    status = "DETECTING" if count else "NO SIGNAL"
    color = (0, 255, 0) if count else (0, 0, 255)

    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (390, 118), (24, 30, 27), -1)
    frame = cv2.addWeighted(overlay, 0.88, frame, 0.12, 0)

    title = "CROPGUARD // LIVE DRONE SIMULATION" if drone_mode else "CROPGUARD // AI VISION"

    cv2.putText(frame, title, (20, 34),
                cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 2)
    cv2.putText(frame, f"STATUS: {status}", (20, 59),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
    cv2.putText(frame, f"FPS: {fps:.1f}   DETECTIONS: {count}", (20, 84),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1)

    if drone_mode:
        cv2.putText(frame, "GPS: LOCKED   |   MISSION: INSPECTING", (20, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.43, (100, 220, 150), 1)

    return frame


def controller_dashboard():
    if page == "Drone Control":
        st.markdown("## Drone Control")
        st.caption("Operational telemetry and mission state.")

        cols = st.columns(5)
        telemetry = [
            ("Status", "ACTIVE", "Connected"),
            ("Battery", f"{DRONE['battery']}%", "Healthy"),
            ("Signal", DRONE["signal"], "Link quality"),
            ("Altitude", f"{DRONE['altitude']} m", "Above field"),
            ("Speed", f"{DRONE['speed']} m/s", "Current"),
        ]
        for col, data in zip(cols, telemetry):
            with col:
                metric_card(*data)

        left, right = st.columns([1.25, 0.75])
        with left:
            section_title("Drone Mission Map", "Simulated GPS position, inspection path and disease hotspots.")
            render_drone_map()

        with right:
            section_title("Drone Status")
            st.markdown(
                f"""
                <div class="status-panel">
                    <div class="status-row"><span>Connection</span><b>{status_badge("Connected")}</b></div>
                    <div class="status-row"><span>Mission</span><b>{status_badge("Inspecting")}</b></div>
                    <div class="status-row"><span>GPS</span><b>{status_badge("Locked")}</b></div>
                    <div class="status-row"><span>Current operation</span><b>Field inspection</b></div>
                    <div class="status-row"><span>Flight time</span><b>{DRONE["flight_time"]}</b></div>
                    <div class="status-row"><span>Current zone</span><b>{DRONE["current_zone"]}</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif page == "Live Mission":
        st.markdown("## Live Mission")
        st.caption("Your original WebRTC + YOLO pipeline is retained here.")
        st.info("The webcam is the current drone-camera simulation. The video transport can later be replaced without redesigning the dashboard.")

        if model is None:
            st.warning("YOLO model not found at `model/best.pt`.")

        webrtc_streamer(
            key="cropguard-live",
            rtc_configuration=RTC_CONFIGURATION,
            video_processor_factory=VideoProcessor,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )

    elif page == "Detection Monitor":
        st.markdown("## Detection Monitor")
        st.caption("Technical detection information for the controller.")

        left, right = st.columns([1.1, 0.9])
        with left:
            section_title("Latest Detection")
            st.markdown(
                f"""
                <div class="technical-card">
                    <div class="tech-line"><span>Detected object</span><b>Tomato Leaf</b></div>
                    <div class="tech-line"><span>Disease</span><b>{FIELD["disease"]}</b></div>
                    <div class="tech-line"><span>Confidence</span><b>{FIELD["confidence"]}%</b></div>
                    <div class="tech-line"><span>Severity</span><b>{FIELD["severity"]}</b></div>
                    <div class="tech-line"><span>Zone</span><b>{FIELD["latest_zone"]}</b></div>
                    <div class="tech-line"><span>Timestamp</span><b>10:42:17</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.session_state.llm:
                st.markdown("### Existing AI Recommendation")
                render_llm_cards(st.session_state.llm)

        with right:
            high_zone = next(z for z in ZONES if z["severity"] == "High")
            section_title("Targeted Spraying", "Simulation only — no real drone command is sent.")
            st.markdown(
                f"""
                <div class="spray-card">
                    <div class="eyebrow">TARGET ZONE</div>
                    <h2>{high_zone["id"]}</h2>
                    <p><b>{high_zone["disease"]}</b></p>
                    <p>Severity: <b>{high_zone["severity"]}</b></p>
                    <p>Estimated area: <b>{high_zone["acre_area"]} acre</b></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("🚁 Initiate Targeted Spray", type="primary", use_container_width=True):
                st.session_state.spray_status = "Locating target..."
                st.rerun()

            sequence = [
                "Locating target...",
                "Drone moving to target...",
                "Target acquired...",
                "Spraying...",
                "Completed ✓",
            ]

            if st.session_state.spray_status != "Ready":
                current = sequence.index(st.session_state.spray_status)
                st.progress(
                    (current + 1) / len(sequence),
                    text=st.session_state.spray_status,
                )
                if current < len(sequence) - 1:
                    if st.button("Simulate Next Step", use_container_width=True):
                        st.session_state.spray_status = sequence[current + 1]
                        st.rerun()
                else:
                    if st.button("Reset", use_container_width=True):
                        st.session_state.spray_status = "Ready"
                        st.rerun()

    elif page == "Inspection History":
        st.markdown("## Inspection History")
        st.dataframe(INSPECTIONS, use_container_width=True, hide_index=True)


# ============================================================
# IMAGE / VIDEO INPUT — ORIGINAL FUNCTIONALITY
# ============================================================
def render_input_lab():
    st.markdown("## AI Vision Input")
    st.caption("Original Image and Video inference retained for testing the trained model.")

    option = st.selectbox("Input Source", ["Image", "Video"])

    if option == "Image":
        file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"], key="lab_image")

        if file:
            img = Image.open(file).convert("RGB")
            frame = np.array(img)

            frame, labels = detect(frame)
            frame = draw_hud(frame, 0, labels)

            st.image(frame, channels="BGR", use_container_width=True)

            if labels:
                st.success(f"Detected: {', '.join(labels)}")

                if st.button("Explain", type="primary"):
                    st.session_state.llm = get_llm_solution(labels[0])
                    st.rerun()

    else:
        file = st.file_uploader("Upload Video", type=["mp4", "mov"], key="lab_video")

        if file:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            tfile.write(file.read())
            tfile.close()

            cap = cv2.VideoCapture(tfile.name)
            frame_window = st.empty()

            prev = time.time()
            fps = 0

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                now = time.time()
                dt = max(now - prev, 1e-6)
                fps = 0.9 * fps + 0.1 * (1 / dt)
                prev = now

                frame, labels = detect(frame)
                frame = draw_hud(frame, fps, labels)
                frame_window.image(frame, channels="BGR")

            cap.release()

def render_llm_cards(raw):
    parsed = parse_llm_response(raw)
    cols = st.columns(3)
    cards = [
        ("🦠 Disease", parsed["Disease Name"], "red"),
        ("⚠️ Cause", parsed["Caused By"], "yellow"),
        ("🌿 Prevention", parsed["Prevention"], "green"),
    ]

    for col, (title, body, accent) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="llm-card {accent}">
                    <h4>{title}</h4>
                    <p>{body or "No information available."}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# MAIN
# ============================================================
if st.session_state.role == "Farmer":
    farmer_dashboard()
else:
    controller_dashboard()

# The original model-testing workflows remain accessible to the
# competition team without contaminating the farmer-facing dashboard.
with st.expander("🔬 Developer / Model Testing"):
    render_input_lab()

st.markdown("---")
st.caption("CropGuard · YOLOv8 + Streamlit + WebRTC · Drone communication and spraying are simulated")
