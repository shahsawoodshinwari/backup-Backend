import os
import numpy as np
import time
import glob
import shutil
import cv2
import pandas as pd

import sqlalchemy
import matplotlib.pyplot as plt

from scipy import spatial
from deepface import DeepFace
from collections import Counter
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import date


def analyze_person(key):
    print("Analyze************************************")
    database_url = 'postgresql://postgres:serG@localhost:5432/pulsse'
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # directory_path = f'C:/Users/DL/Desktop/Pulsses-main/Pulsses-main/Object_Tracking/Images{key}/'
    directory_path = f'/home/ubuntu/Backend/Object_Tracking/Images{key}/'
    


    # f'C:/Users\92333\PycharmProjects\Pulsses\Object_Tracking\Images{key}/'

    person_list = []
    today_date = date.today()
    # GENDER_PROTO =  r"C:\Users\DL\Desktop\Pulsses-main\Pulsses-main\Pulsse\utils\ml_models\deploy_gender.prototxt"
    GENDER_PROTO =  r"/home/ubuntu/Backend/Pulsse/utils/ml_models/deploy_gender.prototxt"
    
    # GENDER_MODEL = r"C:\Users\DL\Desktop\Pulsses-main\Pulsses-main\Pulsse\utils\ml_models\gender_net.caffemodel"
    GENDER_MODEL = r"/home/ubuntu/Backend/Pulsse/utils/ml_models/gender_net.caffemodel"
    GENDER_NET = cv2.dnn.readNet(GENDER_MODEL, GENDER_PROTO)
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    GENDER_LIST = ['Male', 'Female']

    models = [
        "VGG-Face",
        "Facenet",
        "Facenet512",
        "DeepFace",
        "DeepID",
        "ArcFace",
        "Dlib",
        "SFace",
    ]

    def check_for_folder(directory):
        # print("check_for_folder ")
        if os.path.exists(directory) and os.path.isdir(directory):
            return True
        else:
            return False

    def get_images_in_folder(directory_path, folder_path):
        # print("get_images_in_folder ")
        image_files = glob.glob(os.path.join(directory_path, folder_path, '*.jpg'))  # Adjust the pattern if needed
        print(image_files)
        return image_files

    def predict_gender(male, female, s1):
        # print("predict_gender ")
        # result = DeepFace.analyze(s1, actions=['gender'], enforce_detection=False,
        #                           detector_backend = backends[8])
        blob = cv2.dnn.blobFromImage(s1, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        # blobb = blob.reshape(blob.shape[2] * blob.shape[1], blob.shape[3], 1)
        # cv2.imshow('Blob', blobb)
        # cv2.waitKey(5000)
        GENDER_NET.setInput(blob)
        gender_predictions = GENDER_NET.forward()
        gender = GENDER_LIST[gender_predictions[0].argmax()]
        print("Gender: {}, conf: {:.3f}".format(gender, gender_predictions[0].max()))
        if str(gender) == 'Male':
            male = male + 1
        elif str(gender) == 'Female':
            female = female + 1
        return male, female

    def get_embeddings(image):
        print("get_embeddings ")
        image_embedding = DeepFace.represent(image, model_name=models[1], enforce_detection=False)
        return image_embedding[0]['embedding']

    def get_facial_match(id, img_embedding, customers):
        print("fACiali Id=======", id)
        facial_distances = []
        for cust in customers:
            # print("Customer***** ",  cust)
            facial_distance = {'id': '', 'Yolo':'', 'distance': ''}
            result = spatial.distance.cosine(img_embedding, cust.image)
            facial_distance['id'] = int(cust.id)
            facial_distance['Yolo'] = int(id)
            facial_distance['distance'] = result
            facial_distances.append(facial_distance)
        print(facial_distances)
        min_distance_dict = min(facial_distances, key=lambda x: x['distance'])
        if min_distance_dict['distance'] <= 0.45:
            min_distance_dict['match'] = True
            if min_distance_dict['match'] == True:
                print("Dictionary ",min_distance_dict)
            return min_distance_dict
        else:
            min_distance_dict['match'] = False
            return min_distance_dict

    def insert_customer(gender, list_of_embeddings):
        with engine.connect() as connection:
            db_image_str = ', '.join(map(str, list_of_embeddings))
            db_image_str_with_braces = f'{{{db_image_str}}}'
            query = text(
                "INSERT INTO customers (gender, image, facial_recognition_flag, created_at, modified_at) "
                f"VALUES ('{gender}', '{db_image_str_with_braces}',"
                f" '{False}', '{today_date}', '{today_date}') "
            )
            connection.execute(query)
            connection.commit()
    def copy_images_from_folders(source_directory, destination_directory):
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        for folder_name in os.listdir(source_directory):
            folder_path = os.path.join(source_directory, folder_name)
            if os.path.isdir(folder_path):
                image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
                if image_files:
                    image_to_copy = os.path.join(folder_path, image_files[0])
                    destination_path = os.path.join(destination_directory, folder_name + '.jpg')
                    shutil.copy(image_to_copy, destination_path) 

    while True:
        # source_directory = f'C:/Users/DL/Desktop/Pulsses-main/Pulsses-main/Object_Tracking/Images{key}/'
        source_directory = f'/home/ubuntu/Backend/Object_Tracking/Images{key}/'
        # destination_directory = "C:/Users/DL/Desktop/Pulsses-main/Pulsses-main/Object_Tracking/Customer_Images/"
        destination_directory = "/home/ubuntu/Backend/Object_Tracking/Customer_Images/"
        
        copy_images_from_folders(source_directory, destination_directory)
        if check_for_folder(directory_path):
            folder_contents = os.listdir(directory_path)
            folder_contents = sorted(map(float, folder_contents))
            print(folder_contents)
            for id in folder_contents:
                print("Original Folder id", id)
                male = 0
                female = 0
                list_of_embeddings = []
                data = {'yolo_id': int(id), 'customer_id': int(id)} #chnaged from 'customer_id': '' ---> 'customer_id': int(id)
                list_of_images = get_images_in_folder(directory_path, str(id))
                
                for img in list_of_images:
                    img = cv2.imread(img)
                    height = img.shape[0]
                    height_cutoff = height // 4
                    alt_img = img[:height_cutoff, :]
                    # print("Image************", img)
                    kernel = np.array([[0, -1, 0],
                                       [-1, 5, -1],
                                       [0, -1, 0]])
                    # alt_img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
                    # cv2.imshow('img', alt_img)
                    # cv2.waitKey(0)
                    male, female = predict_gender(male, female, alt_img)
                    img_embedding = get_embeddings(img)

                    # list_of_embeddings.append(img_embedding)
                    list_of_embeddings.append((img_embedding))
                    # Write query for visits gender here
                print("Yolo Id ",  id)
                gender = None
                if male > female:
                    data['Gender'] = 'Male' 
                    gender = 'Male'
                elif female > male:
                    data['Gender'] = 'Female'
                    gender = 'Female'
                # query for visits
                with engine.connect() as connection:
                    query = text("UPDATE visits SET gender = :gender_ WHERE yolo_id = :yolo_id")
                    params = {'gender_': gender, 'yolo_id': id}       
                    connection.execute(query, params)
                    connection.commit()
                # ================================
                with engine.connect() as connection:
                    query = text("SELECT * FROM Customers WHERE facial_recognition_flag=True")
                    customers = connection.execute(query)
                    result_set = customers.fetchall()

                if not result_set:
                    insert_customer(gender, list_of_embeddings[0])

                else:
                    match = get_facial_match(id, list_of_embeddings[0], result_set)
                    print("Matched Id*******", match['id'])
                    data['customer_id'] = match['id']
                    print(match)
                    if match['match']:
                          
                        with engine.connect() as connection:
                                query = text(
                                "UPDATE visits SET customer_id = :customer_id WHERE yolo_id = :yolo_id and customer_id is NULL")
                    
                                params = {'customer_id': match['id'], 'yolo_id': match['Yolo']}  
                                
                                connection.execute(query, params)
                                connection.commit()
                               
                    else:
                        insert_customer(gender, list_of_embeddings[0])
                yolo_id_r = float(id)
                directory_to_remove = directory_path+str(yolo_id_r)
                shutil.rmtree(directory_to_remove)
