
# CropGuard — integrated with the existing Smart Plant Disease Detection code

This version preserves the original application's:
- YOLO model at `model/best.pt`
- Image detection
- Video detection
- WebRTC live webcam detection
- OpenRouter disease explanation
- Original multi-object detection logic
- FPS / detection HUD

The product layer adds:
- Farmer / Controller roles
- Farmer field overview
- Simulated severity map
- Disease education
- Inspection history
- Controller telemetry
- Simulated drone mission map
- Detection monitor
- Targeted spraying simulation

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Copy the existing trained model to:

```text
model/best.pt
```

Create `.env` from `.env.example` if OpenRouter explanations are desired.

## Important implementation note

The original WebRTC processor previously attempted to mutate `st.session_state` directly from the WebRTC worker thread. This version deliberately keeps the worker thread focused on frame inference/rendering. That avoids coupling the real-time video callback to Streamlit UI state.

The original Image/Video workflows are also retained under **Developer / Model Testing**, so the trained model can still be tested independently of the product dashboards.
