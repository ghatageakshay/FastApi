from app.database import SessionLocal
from app.models.patient import Patient

db = SessionLocal()

patient = Patient(
    first_name = "Akshay",
    middle_name = "Praveen",
    last_name = "Ghatage",
    age = 21,
    email = "ghatageakshay96@gmail.com",
    weight = 53,
    height = 1.77
)

db.add(patient)
db.commit()
db.refresh(patient)

print(patient.id)

db.close()