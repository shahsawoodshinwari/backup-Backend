from datetime import date

from Pulsse.database import db
from sqlalchemy.dialects.postgresql import ARRAY
class TempTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    fullname = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    day = db.Column(db.Date(), nullable=True)
    time_in = db.Column(db.Time(), nullable=True)
    time_out = db.Column(db.Time(), nullable=True)
    group_val = db.Column(db.Boolean(), nullable=True)