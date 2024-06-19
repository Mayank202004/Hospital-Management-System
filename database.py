import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    #============================= Fetch Default Tables for various windows ====================================================
    #To fetch default doctors data
    def fetch_doctors_data(self):
        self.cursor.execute('SELECT * FROM doctors')
        data = self.cursor.fetchall()
        return data
    #To fetch default default patients table
    def fetch_patients_data(self):
        self.cursor.execute('SELECT * FROM Patients')
        data = self.cursor.fetchall()
        return data
    #To fetch default appointments table
    def fetch_appointments(self):
        self.cursor.execute('''SELECT a.AppointmentID,a.PatientID,p.Name AS patient_name,a.DoctorID,'Dr. ' || d.first_name AS doctor_name,a.AppointmentDate,a.Reason,a.Status FROM Appointments a INNER JOIN Patients p ON a.PatientID = p.PatientID INNER JOIN Doctors d ON a.DoctorID = d.doctor_id''')
        data = self.cursor.fetchall()
        return data
    #To fetch default wards table
    def fetch_wards_data(self):
        self.cursor.execute("select * from Wards")
        data = self.cursor.fetchall()
        return data
    #To fetch Departments table
    def fetch_departments_data(self):
        self.cursor.execute("SELECT d.DepartmentID, d.DepartmentName, d.HeadOfDepartment, 'Dr. ' || doc.first_name AS HODName FROM Departments d INNER JOIN Doctors doc ON d.HeadOfDepartment = doc.doctor_id")
        data = self.cursor.fetchall()
        return data
    #To fetch default beds table
    def fetch_beds_data(self):
        self.cursor.execute("SELECT b.BedID, b.WardID, w.WardName, b.BedNumber, b.Availability, b.PatientID, p.Name AS PatientName FROM Beds b LEFT JOIN Wards w ON b.WardID = w.WardID LEFT JOIN Patients p ON b.PatientID = p.PatientID")
        data = self.cursor.fetchall()
        return data
    #To fetch default Medicine table
    def fetch_medicine_data(self):
        self.cursor.execute("SELECT * from Medicines")
        data = self.cursor.fetchall()
        return data
    #To fetch default Lab Tests table
    def fetch_labtests_data(self):
        self.cursor.execute("SELECT l.TestID, l.TestName,l.TestCost, l.DepartmentID, d.DepartmentName from Labtests l INNER JOIN Departments d on l.DepartmentID=d.DepartmentID")
        data = self.cursor.fetchall()
        return data
    #To fetch default Lab Results table
    def fetch_labresults_data(self):
        self.cursor.execute("SELECT r.ResultID,r.TestID, l.TestName,r.PatientID,p.Name, r.ResultDate, r.ResultDetails from LabResults r INNER JOIN LabTests l on r.TestID=l.TestID INNER JOIN Patients p ON r.PatientID = p.PatientID")
        data = self.cursor.fetchall()
        return data
    
    #To fetch prescription of given id
    def fetch_prescription_data(self,id):
        self.cursor.execute(f"SELECT  p.MedicineID, m.MedicineName, m.Price, p.Instructions FROM Prescriptions p INNER JOIN Medicines m ON p.MedicineID = m.MedicineID where p.PrescriptionID={id}")
        data = self.cursor.fetchall()
        return data
    
    #To fetch prescription of given id
    def fetch_prescription_details(self,id):
        self.cursor.execute(f"SELECT 'Dr. ' || d.first_name as doctor_name,p.Name,SUM(m.Price) AS TotalPrice FROM Prescriptions a INNER JOIN Medicines m ON a.MedicineID = m.MedicineID INNER JOIN Patients p on a.PatientID=p.PatientID INNER JOIN Doctors d on a.DoctorID=d.doctor_id where a.PrescriptionID={id} GROUP BY a.PrescriptionID, a.PatientID, a.DoctorID")
        data = self.cursor.fetchall()
        return data
    
    # ========================================== PopUp Windows searchby Query ===================================
    #used for find patients window in manage appointments
    def search_patients(self,searchby,str):
        self.cursor.execute(f"select PatientID,Name from Patients where {searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    #used for find Doctors window in manage appointments
    def search_doctors(self,searchby,str):
        self.cursor.execute(f"SELECT doctor_id, 'Dr. ' || first_name AS doctor_name,specialization,department FROM Doctors where {searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    
    #used for find medicines window in add prescription
    def search_Medicines(self,searchby,str):
        self.cursor.execute(f"SELECT MedicineID,MedicineName,Manufacturer,Price,MRP FROM Medicines where {searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    
#used for find department window in add Test Window
    def search_department(self,searchby,str):
        self.cursor.execute(f"SELECT DepartmentID,DepartmentName from Departments where {searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    
    #used for find ward in add bed Window
    def search_wards(self,searchby,str):
        self.cursor.execute(f"SELECT WardID, WardName, WardType from Wards where {searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    
    #used for find Tests  in add TestResult Window
    def search_tests(self,searchby,str):
        if searchby=="DepartmentName":
            svar='d'
        else:
            svar='l'
        self.cursor.execute(f"SELECT l.TestID,l.TestName,d.DepartmentName from LabTests l inner join Departments d on l.DepartmentID=d.DepartmentID where {svar}.{searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data

    #used for find Doctors window in manage appointments
    def search_p(self,searchby,str):
        if searchby in ['PatientID','DoctorID']:
            svar='a'

        elif searchby in ['Name']:
            svar='p'
        elif searchby in ['first_name']:
            svar='d'
        self.cursor.execute(f"SELECT a.PrescriptionID,a.DoctorID,'Dr. ' || d.first_name as doctor_name,a.PatientID,p.Name,SUM(m.Price) AS TotalPrice FROM Prescriptions a INNER JOIN Medicines m ON a.MedicineID = m.MedicineID INNER JOIN Patients p on a.PatientID=p.PatientID INNER JOIN Doctors d on a.DoctorID=d.doctor_id where {svar}.{searchby} like '%{str}%' GROUP BY a.PrescriptionID, a.PatientID, a.DoctorID")
        data = self.cursor.fetchall()
        return data
    
    # ===========================searchby for main windows (patients/doctors/wards/beds etc) ===================================
    def searchby_patients(self,searchby,str):
        self.cursor.execute(f"select * from Patients where {searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    def searchby_doctors(self,searchby,str):
        self.cursor.execute(f"select * from Doctors where {searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    def searchby_appointments(self,searchby,str):
        if searchby in ["PatientID", "Name"]:
            svar='p'
        elif searchby in ["first_name"]:
            svar='d'
        else: svar='a'
        self.cursor.execute(f"SELECT a.AppointmentID,a.PatientID,p.Name AS patient_name,a.DoctorID,'Dr. ' || d.first_name AS doctor_name,a.AppointmentDate,a.Reason,a.Status FROM Appointments a INNER JOIN Patients p ON a.PatientID = p.PatientID INNER JOIN Doctors d ON a.DoctorID = d.doctor_id where {svar}.{searchby} like '%{str}%' ")
        data = self.cursor.fetchall()
        return data
    def searchby_wards(self,searchby,str):
        self.cursor.execute(f"select * from Wards where {searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    def searchby_dept(self,searchby,str):
        self.cursor.execute(f"SELECT d.DepartmentID, d.DepartmentName, d.HeadOfDepartment, 'Dr. ' || doc.first_name AS HODName FROM Departments d INNER JOIN Doctors doc ON d.HeadOfDepartment = doc.doctor_id where d.{searchby} like '%{str}%'")
        data=self.cursor.fetchall()
        return data
    def searchby_beds(self,searchby,str):
        if searchby in ["PatientID", "Name", "ContactNumber"]:
            svar='p'
        elif searchby in ["WardID","WardName","WardType"]:
            svar='w'
        else: svar='b'
        self.cursor.execute(f"SELECT b.BedID, b.WardID, w.WardName, b.BedNumber, b.Availability, b.PatientID, p.Name AS PatientName FROM Beds b LEFT JOIN Wards w ON b.WardID = w.WardID LEFT JOIN Patients p ON b.PatientID = p.PatientID where {svar}.{searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    def searchby_medicines(self,searchby,str):
        self.cursor.execute(f"select * from Medicines where {searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    def searchby_labtests(self,searchby,str):
        if searchby=="DepartmentName":
            svar='d'
        else:
            svar='l'
        self.cursor.execute(f"SELECT l.TestID, l.TestName,l.TestCost, l.DepartmentID, d.DepartmentName from Labtests l INNER JOIN Departments d on l.DepartmentID=d.DepartmentID where {svar}.{searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    def searchby_labresults(self,searchby,str):
        svar='r'
        if searchby=="Name":
            svar='p'
        elif searchby=="TestName":
            svar='l'
        self.cursor.execute(f"SELECT r.ResultID,r.TestID, l.TestName,r.PatientID,p.Name, r.ResultDate, r.ResultDetails from LabResults r INNER JOIN LabTests l on r.TestID=l.TestID INNER JOIN Patients p ON r.PatientID = p.PatientID where {svar}.{searchby} like '%{str}%'")
        data = self.cursor.fetchall()
        return data
    
    #=================================== Fetch Patient Name and Doctor Name for Appointment Window ==============================
    def get_patient_name(self,id):
        self.cursor.execute(f"SELECT Name FROM Patients WHERE PatientID={id}")
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
            
    def get_doctor_name(self,id):
        self.cursor.execute(f"SELECT 'Dr. ' || first_name FROM Doctors WHERE doctor_id={id}")
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def get_medicine_name(self,id):
        self.cursor.execute(f"SELECT MedicineName,Price FROM Medicines WHERE MedicineID={id}")
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return None    

    def getprescriptionID(self):
        #prescription id to add new prescription
        # +1 so that we get new id for new insertion
        self.cursor.execute("select max(PrescriptionID)+1 from Prescriptions")
        result = self.cursor.fetchone()
        return result[0] if result else 1
    
    def getWardID(self):
        #ward id to add new prescription
        # +1 so that we get new id for new ward
        self.cursor.execute("select max(WardID)+1 from Wards")
        result = self.cursor.fetchone()
        return result[0] if result else 1
    
    def get_department_name(self,id):
        self.cursor.execute(f"SELECT DepartmentName FROM Departments WHERE DepartmentID={id}")
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return None
        
    def get_ward_name(self,id):
        self.cursor.execute(f"SELECT WardName FROM Wards WHERE WardID={id}")
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return None 

    def get_test_name(self,id):
        self.cursor.execute(f"SELECT TestName FROM LabTests WHERE TestID={id}")
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return None  

    # ====================Insert to table queries==============================
    def insertPatient(self,values):
        self.cursor.execute(f"INSERT INTO Patients (Name, DateOfBirth, Gender, ContactNumber, Email, BloodType, InsuranceProvider, EmergencyContactName, EmergencyContactNumber, Allergies, MedicalHistory) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
        self.conn.commit()

    def insertDoctor(self, values):
        self.cursor.execute("INSERT INTO Doctors (first_name, last_name, specialization, contact_number, email,address, gender, date_of_birth, joining_date, qualification,experience, department) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
        self.conn.commit()

    def insertAppointment(self, values):
        self.cursor.execute("INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate, Reason, Status) VALUES (?, ?, ?, ?, ?)", values)
        self.conn.commit()
    
    def insertMedicine(self, values):
        self.cursor.execute("INSERT INTO Medicines (MedicineName, Manufacturer, Price, MRP, Quantity) VALUES (?, ?, ?, ?, ?)", values)
        self.conn.commit()

    def insertPrescription(self,values):
        self.cursor.executemany("INSERT INTO Prescriptions (PrescriptionID, DoctorID, PatientID, PrescriptionDate, Instructions, MedicineID) VALUES (?, ?, ?, ?, ?, ?)",values)
        self.conn.commit()

    def insertTest(self,values):
        self.cursor.execute("INSERT INTO LabTests (TestName, TestCost, DepartmentID) VALUES (?, ?, ?)",values)
        self.conn.commit()

    def insertTestResult(self,values):
        self.cursor.execute("INSERT INTO LabResults (TestID, PatientID, ResultDate, ResultDetails) VALUES (?, ?, ?, ?)",values)
        self.conn.commit()

    def insertWard(self,values):
        self.cursor.execute("INSERT INTO Wards (WardName, WardType, Capacity) VALUES (?, ?, ?)",values)
        self.conn.commit() 

    def insertBed(self,values):
        self.cursor.execute("INSERT INTO Beds (WardID, BedNumber, Availability, PatientID) VALUES (?, ?, ?, ?)",values)
        self.conn.commit() 

    def insertDepartment(self,values):
        self.cursor.execute("INSERT INTO Departments (DepartmentName, HeadOfDepartment) VALUES (?, ?)",values)
        self.conn.commit() 

    # ====================Update table element queries==============================
    def updatePatient(self, values, identifier):
        self.cursor.execute(f"UPDATE Patients SET Name=?, DateOfBirth=?, Gender=?, ContactNumber=?, Email=?, BloodType=?, InsuranceProvider=?, EmergencyContactName=?, EmergencyContactNumber=?, Allergies=?, MedicalHistory=? WHERE PatientID={identifier}", values)
        self.conn.commit()

    def updateDoctor(self, values, identifier):
        self.cursor.execute(f"UPDATE Doctors SET first_name=?, last_name=?, specialization=?, contact_number=?,email=?, address=?, gender=?, date_of_birth=?, joining_date=?,qualification=?, experience=?, department=? WHERE doctor_id={identifier}", values)
        self.conn.commit()

    def updateAppointment(self, values, identifier):
        self.cursor.execute(f"UPDATE Appointments SET PatientID=?, DoctorID=?, AppointmentDate=?, Reason=?, Status=? WHERE AppointmentID={identifier}",values)
        self.conn.commit()
    
    def updateMedicine(self, values, identifier):
        self.cursor.execute(f"UPDATE Medicines SET MedicineName=?, Manufacturer=?, Price=?, MRP=?,Quantity=? WHERE MedicineID={identifier}", values)
        self.conn.commit()
    
    def updateTest(self, values, identifier):
        self.cursor.execute(f"UPDATE LabTests SET TestName=?, TestCost=?, DepartmentID=? WHERE TestID={identifier}", values)
        self.conn.commit()

    def updateTestResult(self, values, identifier):
        self.cursor.execute(f"UPDATE LabResults SET TestID=?, PatientID=?, ResultDate=?, ResultDetails=? WHERE ResultID={identifier}", values)
        self.conn.commit()

    def updateWard(self, values, identifier):
        self.cursor.execute(f"UPDATE Wards SET WardName=?, WardType=?, Capacity=? WHERE WardID={identifier}", values)
        self.conn.commit()

    def updateBed(self, values, identifier):
        self.cursor.execute(f"UPDATE Beds SET WardID=?, BedNumber=?, Availability=?, PatientID=? WHERE BedID={identifier}", values)
        self.conn.commit()

    def updateDepartment(self, values, identifier):
        self.cursor.execute(f"UPDATE Departments SET DepartmentName=?, HeadOfDepartment=? WHERE DepartmentID={identifier}", values)
        self.conn.commit()

    # ====================Delete table element queries==============================
    def deletePatient(self,identifier):
        self.cursor.execute(f"DELETE FROM Patients where PatientID={identifier}")
        self.conn.commit()
    
    def deleteDoctor(self,identifier):
        self.cursor.execute(f"DELETE FROM Doctors where doctor_id={identifier}")
        self.conn.commit()

    def deleteAppointment(self, identifier):
        self.cursor.execute(f"DELETE FROM Appointments WHERE AppointmentID={identifier}")
        self.conn.commit()
    
    def deleteMedicine(self,identifier):
        self.cursor.execute(f"DELETE FROM Medicines where MedicineID={identifier}")
        self.conn.commit()

    def deleteTest(self,identifier):
        self.cursor.execute(f"DELETE FROM LabTests where TestID={identifier}")
        self.conn.commit()

    def deleteTestResult(self,identifier):
        self.cursor.execute(f"DELETE FROM LabResults where ResultID={identifier}")
        self.conn.commit()

    def deleteWard(self,identifier):
        self.cursor.execute(f"DELETE FROM Wards where WardID={identifier}")
        self.conn.commit()

    def deleteBed(self,identifier):
        self.cursor.execute(f"DELETE FROM Beds where BedID={identifier}")
        self.conn.commit()

    def deleteDepartment(self,identifier):
        self.cursor.execute(f"DELETE FROM Departments where DepartmentID={identifier}")
        self.conn.commit()


    #================= Login Logic =========================================
    
    def verify_user(self,username,password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = self.cursor.fetchone()
        # If result is not None, the user is verified
        if result:
            return True
        else:
            return False





    def close_connection(self):
        self.cursor.close()
        self.conn.close()
