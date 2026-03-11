# 🥔 Potato Disease Detection

AI-powered potato leaf disease detection using a Custom CNN built with PyTorch and deployed with Streamlit.

## 🌟 Features

- **3-Class Classification**: Early Blight, Late Blight, Healthy
- **Real-time Inference**: Upload a leaf image and get instant predictions
- **Disease Information**: Actionable treatment recommendations for detected diseases

## 🛠️ Tech Stack

- **Deep Learning**: PyTorch (Custom CNN)
- **Frontend**: Streamlit
- **Image Processing**: Pillow, TorchVision

## 🚀 Deployment

### Option 1: Streamlit Community Cloud (Recommended)

1. Fork/clone this repo
2. Upload `potato_disease_model.pth` to Google Drive and get a shareable link
3. Extract the file ID from the link (e.g., `https://drive.google.com/file/d/<FILE_ID>/view`)
4. On [Streamlit Cloud](https://share.streamlit.io/):
   - Connect your GitHub repo
   - Set **Main file path** to `app.py`
   - Add secret: `MODEL_GDRIVE_ID = "<YOUR_FILE_ID>"`
5. Deploy!

### Option 2: Local Setup

```bash
# Clone the repository
git clone https://github.com/Rudra627/potato-disease-detection.git
cd potato-disease-detection

# Install dependencies
pip install -r requirements.txt

# Place the model file in the project root
# (potato_disease_model.pth)

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
├── app.py                          # Streamlit web application
├── predict.py                      # Model definition & inference logic
├── PotatoDiseaseClassification.ipynb  # Training notebook
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## ⚠️ Model Weights

The trained model file (`potato_disease_model.pth`, ~200MB) is **not included** in the repository due to GitHub's file size limits.

**To set up the model for deployment:**
1. Upload `potato_disease_model.pth` to Google Drive
2. Make it shareable (Anyone with the link)
3. Set the `MODEL_GDRIVE_ID` environment variable to the file ID
4. The app will auto-download the model on first run

## 📜 License

This project is for educational purposes.
