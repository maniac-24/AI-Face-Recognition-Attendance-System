import streamlit as st
import torch
import cv2
import numpy as np
from ultralytics import YOLO
from facenet_pytorch import InceptionResnetV1

@st.cache_resource
def load_models():
    yolo = YOLO("models/yolov8n.pt")
    facenet = InceptionResnetV1(pretrained='vggface2').eval()
    return yolo, facenet

yolo, facenet = load_models()


def get_embedding(face):
    face = cv2.resize(face, (160, 160)) / 255.0
    face = torch.tensor(face).permute(2, 0, 1).unsqueeze(0).float()

    with torch.no_grad():
        emb = facenet(face).numpy()[0]

    return emb / np.linalg.norm(emb)


def recognize(embedding, users, threshold=0.75):
    best, score = None, -1

    for uid, name, emb in users:
        sim = np.dot(embedding, emb) / (
            np.linalg.norm(embedding) * np.linalg.norm(emb)
        )
        if sim > score:
            best, score = (uid, name), sim

    if score > threshold:
        return best, score

    return None, score