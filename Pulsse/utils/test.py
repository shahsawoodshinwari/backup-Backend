import cv2
import os
from ultralytics import YOLO
from datetime import datetime
# from Pulsse.database import db
# from Pulsse.models.visits import Visits



username = 'admin'
password = 'hik@12345'
ip = '172.23.16.55'
address = f'rtsp://{username}:{password}@{ip}'


model = YOLO('yolov8n.pt')
exit_list = []
results_generator = model.track(source=address, classes=0,
                                    stream=True, persist=True, conf=0.5)


while True:
        results = next(results_generator, None)
        
        print(results.boxes.id)
        
        scale_percent = 20
        frame = results.plot()
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        cv2.line(frame, (2000, 600), (100, 600), (0, 255, 0), 2)
        cv2.line(frame, (2000, 900), (100, 900), (0, 255, 0), 2)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("YOLOv8 Inference", resized)

        if cv2.waitKey(500) & 0xFF == ord('q'):
            break
        print("Results", results.boxes.id)
        if results.boxes.id is not None:

            box = results.boxes.xyxy.tolist()
            id = results.boxes.id.tolist()
            frame_counting_buffer = dict(zip(id, box))
            print(frame_counting_buffer)

            frame_counting_buffer = {key: frame_counting_buffer[key] for key in frame_counting_buffer.keys()
                                        if str(key) not in exit_list}
            frame_counting_buffer = {key: values for key, values in frame_counting_buffer.items() if
                                        values[3] > 600}
            exit_list = list(set(exit_list))
            print("Exit_list", exit_list)

            base_directory = "C:\\Users\\DL\\Desktop\\Pulsses-main\\Pulsses-main\\Object_Tracking\\Images1"
            for idx, values in frame_counting_buffer.items():
                folder_names = os.listdir(base_directory)
                if str(idx) not in folder_names:
                    if values[3] > 900:
                        print("Exit")
                        exit_list.append(str(idx))
                        # with pulsse_app.app_context():
                        #     visit = Visits()
                        #     visit.yolo_id = int(idx)
                        #     visit.sitekey = key
                        #     visit.time_out = datetime.now().time()
                        #     if len(frame_counting_buffer) > 1:
                        #         visit.group_val = True
                        #     db.session.add(visit)
                        #     db.session.commit()
                    else:
                        os.mkdir(os.path.join(base_directory, str(idx)))
                        print("Enter")
                        # with pulsse_app.app_context():
                            # visit = Visits()
                            # visit.yolo_id = int(idx)
                            # visit.sitekey = key
                            # visit.time_in = datetime.now().time()
                            # if len(frame_counting_buffer) > 1:
                            #     visit.group_val = True
                            # db.session.add(visit)
                            # db.session.commit()
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


