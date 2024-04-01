import cv2
import os
from ultralytics import YOLO
from datetime import datetime
from Pulsse.database import db
from Pulsse.models.visits import Visits

import sys

# username = 'admin'
# password = 'hik@12345'
# ip = '172.23.16.55'
# address = f'rtsp://{username}:{password}@{ip}'


# address = "https://isgpopen.ezvizlife.com/v3/openlive/AA4823505_1_1.m3u8?expire=1740389224&id=681915081060884480&c=3cffb6de2e&t=0e07e0e9b4a4b94668091c2018d817b79bbf461cf097ad3a6fe2bc5f375a765e&ev=100"
address = "https://isgpopen.ezvizlife.com/v3/openlive/AB9438217_1_1.m3u8?expire=1711995421&id=694716923277819904&c=a38fde48c5&t=e05e0d4111071bfff584e1484a85ce600f34d0b28caa58986ff5f9e404ff98ed&ev=100"

def extract_person_site_2(key, pulsse_app):
    # address = url
    model = YOLO('yolov8n.pt')
    exit_list = []
    results_generator = model.track(source=address, classes=0,
                                    stream=True, persist=True, conf=0.5)

    while True:
        results = next(results_generator, None)
        print(results.boxes.id)

        scale_percent = 40
        frame = results.plot()
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        start_point = (800, 50)
        end_point = (434, 50)
        color = (103, 255, 0)
        thickness = 5
        cv2.line(resized , start_point, end_point, color,  thickness)
        # cv2.imshow("stream2", resized)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if results.boxes.id is not None:

            box = results.boxes.xyxy.tolist()
            id = results.boxes.id.tolist()
            print('original', id )
            frame_counting_buffer = dict(zip(id, box))
            print(frame_counting_buffer)

            frame_counting_buffer = {key: frame_counting_buffer[key] for key in frame_counting_buffer.keys()
                                        if str(key) not in exit_list}
            frame_counting_buffer = {key: values for key, values in frame_counting_buffer.items() if
                                        values[3] > 700}   # 698
            # print("Frame Counting")
            # print(frame_counting_buffer)
            

            exit_list = list(set(exit_list))

            # base_directory = "C:\\Users\\DL\\Desktop\\Pulsses-main\\Pulsses-main\\Object_Tracking\\Images2"
            base_directory = "/home/ubuntu/Backend/Object_Tracking/Images2"
            for idx, values in frame_counting_buffer.items():
                folder_names = os.listdir(base_directory)
                if str(idx) not in folder_names:
                    if values[3] > 850: #848
                        print("Exit")
                        exit_list.append(str(idx))
                        with pulsse_app.app_context():
                            visit = Visits()
                            visit.yolo_id = int(idx)
                            visit.sitekey = key
                            visit.time_out = datetime.now().time()
                            if len(frame_counting_buffer) > 1:
                                visit.group_val = True
                            db.session.add(visit)
                            db.session.commit()
                    else:
                        os.mkdir(os.path.join(base_directory, str(idx)))
                        with pulsse_app.app_context():
                            visit = Visits()
                            visit.yolo_id = int(idx)
                            visit.sitekey = key
                            visit.time_in = datetime.now().time()
                            if len(frame_counting_buffer) > 1:
                                visit.group_val = True
                            db.session.add(visit)
                            db.session.commit()
                        output_path = os.path.join(base_directory, str(idx),
                                                f"{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
                        if len(os.listdir(os.path.join(base_directory, str(idx)))) < 7:
                            img = frame[int(values[1]):int(values[3]), int(values[0]):int(values[2])]
                            cv2.imwrite(output_path, img)
                else:
                    output_path = os.path.join(base_directory, str(idx),
                                                f"{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
                    if len(os.listdir(os.path.join(base_directory, str(idx)))) < 7:
                        img = frame[int(values[1]):int(values[3]), int(values[0]):int(values[2])]
                        cv2.imwrite(output_path, img)
                    else:
                        pass




# import cv2
# import os
# from ultralytics import YOLO
# from datetime import datetime
# from Pulsse.database import db
# from Pulsse.models.visits import Visits



# username = 'admin'
# password = 'hik@12345'
# ip = '172.23.16.55'
# address = f'rtsp://{username}:{password}@{ip}'


# def extract_person(key, pulsse_app):
#     model = YOLO('yolov8n.pt')
#     exit_list = []
#     results_generator = model.track(source=address, classes=0,
#                                     stream=True, persist=True, conf=0.5)

#     while True:
#         results = next(results_generator, None)
#         print(results.boxes.id)

#         scale_percent = 20
#         frame = results.plot()
#         width = int(frame.shape[1] * scale_percent / 100)
#         height = int(frame.shape[0] * scale_percent / 100)
#         dim = (width, height)
#         resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
#         cv2.imshow("YOLOv8 Inference", resized)

#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

#         if results.boxes.id is not None:

#             box = results.boxes.xyxy.tolist()
#             id = results.boxes.id.tolist()
#             print('original', id )
#             frame_counting_buffer = dict(zip(id, box))
#             print(frame_counting_buffer)

#             frame_counting_buffer = {key: frame_counting_buffer[key] for key in frame_counting_buffer.keys()
#                                         if str(key) not in exit_list}
#             frame_counting_buffer = {key: values for key, values in frame_counting_buffer.items() if
#                                         values[3] > 800}
#             exit_list = list(set(exit_list))

#             base_directory = "C:\\Users\\DL\\Desktop\\Pulsses-main\\Pulsses-main\\Object_Tracking\\Images1"
#             for idx, values in frame_counting_buffer.items():
#                 folder_names = os.listdir(base_directory)
#                 if str(idx) not in folder_names:
#                     if values[3] > 950:
#                         print("Exit")
#                         exit_list.append(str(idx))
#                         with pulsse_app.app_context():
#                             visit = Visits()
#                             visit.yolo_id = int(idx)
#                             visit.sitekey = key
#                             visit.time_out = datetime.now().time()
#                             if len(frame_counting_buffer) > 1:
#                                 visit.group_val = True
#                             db.session.add(visit)
#                             db.session.commit()
#                     else:
#                         os.mkdir(os.path.join(base_directory, str(idx)))
#                         with pulsse_app.app_context():
#                             visit = Visits()
#                             visit.yolo_id = int(idx)
#                             visit.sitekey = key
#                             visit.time_in = datetime.now().time()
#                             if len(frame_counting_buffer) > 1:
#                                 visit.group_val = True
#                             db.session.add(visit)
#                             db.session.commit()
#                         output_path = os.path.join(base_directory, str(idx),
#                                                 f"{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
#                         if len(os.listdir(os.path.join(base_directory, str(idx)))) < 7:
#                             img = frame[int(values[1]):int(values[3]), int(values[0]):int(values[2])]
#                             cv2.imwrite(output_path, img)
#                 else:
#                     output_path = os.path.join(base_directory, str(idx),
#                                                 f"{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
#                     if len(os.listdir(os.path.join(base_directory, str(idx)))) < 7:
#                         img = frame[int(values[1]):int(values[3]), int(values[0]):int(values[2])]
#                         cv2.imwrite(output_path, img)
#                     else:
#                         pass