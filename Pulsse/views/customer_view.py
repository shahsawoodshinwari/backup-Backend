import cv2
import numpy as np

from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
from deepface import DeepFace
from sqlalchemy import exc, desc, func
from flask_jwt_extended import jwt_required


from sqlalchemy.orm import joinedload

from Pulsse.database import db
from Pulsse.models.customers import Customers
from Pulsse.models.tempTable import TempTable
from Pulsse.models.visits import Visits
customer_blueprint = Blueprint('customer', __name__, url_prefix='/customer')


@customer_blueprint.route('/add', methods=['POST'])
@jwt_required()
def add_customer():
    name = request.form.get('name')
    gender = request.form.get('gender')
    image = request.files.get('image')
    file_bytes = np.fromfile(image, np.uint8)
    file = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    try:
        image_embedding = DeepFace.represent(file, model_name="Facenet")
        print(image_embedding)
    except:
        return jsonify(error=True, msg="Face Not Detected"), 400

    customer = Customers()
    customer.name = (name.strip()).lower()
    customer.gender = gender.lower()
    customer.facial_recognition_flag = True
    customer.image = image_embedding[0]['embedding']

    try:
        db.session.add(customer)
        db.session.commit()
    except exc.SQLAlchemyError as err:
        return jsonify(error=True, msg=str(err)), 400

    return jsonify(error=False, msg="Customer Successfully Added"), 200


@customer_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_customer():

    customer_data = []

            
    # Query Visits table based on the condition customer.id == customer_id
    visits = Visits.query.order_by(Visits.created_at.desc()).all()
    

    for visitor in visits:
        # if visitor.customer_id == customer.id:
            customer_data.append({
                'visitDate': str(visitor.created_at),
                'gender': str(visitor.gender),
                'group': str(visitor.group_val),
                'timein': str(visitor.time_in),
                'timeout': str(visitor.time_out)
            })
    
    return jsonify(error=False, msg="Successfully Displayed", data=customer_data)

    # =============================== second=======================
    # customer_data = []
    # customers = Customers.query.filter(Customers.facial_recognition_flag).order_by(Customers.created_at.desc()).all()
    # for customer in customers:
    #     customer_id = customer.id
            
    #     # Query Visits table based on the condition customer.id == customer_id
    #     visits = Visits.query.filter_by(customer_id=customer_id).order_by(Visits.created_at.desc()).all()
        
    
    #     for visitor in visits:
    #         # if visitor.customer_id == customer.id:
    #             customer_data.append({
    #                 'visitDate': str(visitor.created_at),
    #                 'gender': customer.gender,
    #                 'group': str(visitor.group_val),
    #                 'timein': str(visitor.time_in),
    #                 'timeout': str(visitor.time_out)
    #             })

    # return jsonify(error=False, msg="Successfully Displayed", data=customer_data)


    # ================================== The Original ====================================== 

    # customer_data = []
    # customers = Customers.query.filter(Customers.facial_recognition_flag).all()

    # for customer in customers:
    #     customer_id = customer.id
        
    #     # Query Visits table based on the condition customer.id == customer_id
    #     visits = Visits.query.filter_by(customer_id=customer_id).all()

    
    # print(len(visits))
    # for visitor in visits:
       
    #     for customer in customers:
    #         if  visitor.customer_id == customer.id:
    #             customer_data.append({ 'visitDate': str(visitor.created_at),'gender': customer.gender, 'group': str(visitor.group_val), 'timein': str(visitor.time_in), 'timeout': str(visitor.time_out) })
    # return jsonify(error=False, msg="Successfully Displayed", data=customer_data)








# ================ Original one ====================
    # customer_data = []
    # customers = Customers.query.filter(Customers.facial_recognition_flag).all()

    # for customer in customers:
    #     customer_id = customer.id
        
    #     # Query Visits table based on the condition customer.id == customer_id
    #     visits = Visits.query.filter_by(customer_id=customer_id).all()

    #     # Append relevant information to customer_data
    #     for visit in visits:
    #         customer_data.append({
    #             'id': str(customer.id),
    #             'fullname': customer.name,
    #             'gender': customer.gender,
    #             'day': visit.day,
    #             'time_in': visit.time_in,
    #             'time_out': visit.time_out,
    #             'group_val': visit.group_val
    #         })

    # return jsonify(error=False, msg="Successfully Displayed", data=customer_data)
