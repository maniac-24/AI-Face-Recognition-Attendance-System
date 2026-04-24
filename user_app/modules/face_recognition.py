import torch
import cv2
import numpy as np
from ultralytics import YOLO
from facenet_pytorch import InceptionResnetV1
import streamlit as st


# ---------------- LOAD MODELS (CACHED) ---------------- #
@st.cache_resource
def load_models():
    yolo_model = YOLO("yolov8n.pt")  # lightweight model
    facenet_model = InceptionResnetV1(pretrained='vggface2').eval()
    return yolo_model, facenet_model


yolo, facenet = load_models()


# ---------------- GET EMBEDDING ---------------- #
def get_embedding(face_img):
    try:
        # Resize
        face = cv2.resize(face_img, (160, 160))

        # BGR → RGB
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

        # Convert to float
        face = face.astype(np.float32)

        # 🔥 FaceNet normalization (IMPORTANT)
        mean, std = face.mean(), face.std()
        face = (face - mean) / std

        # HWC → CHW
        face = np.transpose(face, (2, 0, 1))

        # To tensor
        face = torch.tensor(face).unsqueeze(0)

        # Get embedding
        with torch.no_grad():
            embedding = facenet(face)

        embedding = embedding.squeeze().numpy()

        # 🔥 Normalize embedding (CRITICAL)
        embedding = embedding / np.linalg.norm(embedding)

        return embedding

    except Exception as e:
        print("Embedding error:", e)
        return None