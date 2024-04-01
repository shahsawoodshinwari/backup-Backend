from deepface import DeepFace
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]
result = DeepFace.verify(img1_path = r"C:/Users\DL\Downloads/uzair.jpg", img2_path= r"C:/Users\DL\Desktop/Pulsses-main/Pulsses-main/Object_Tracking/Images1/48.0/20240105150405.jpg",
                         model_name = models[1], enforce_detection=False)
print(result)