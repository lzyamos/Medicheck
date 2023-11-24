from django.db import models

class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    RegistrationDate = models.DateTimeField(auto_now_add=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Phone = models.CharField(max_length=15)

    def __str__(self):
        return self.Username

class Symptom(models.Model):
    SymptomID = models.AutoField(primary_key=True)
    SymptomName = models.CharField(max_length=100)
    Description = models.TextField()

    def __str__(self):
        return self.SymptomName

class UserSymptom(models.Model):
    UserSymptomID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    SymptomID = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    Severity = models.IntegerField()
    Timestamp = models.DateTimeField(auto_now_add=True)

class Condition(models.Model):
    ConditionID = models.AutoField(primary_key=True)
    ConditionName = models.CharField(max_length=100)
    Description = models.TextField()

    def __str__(self):
        return self.ConditionName

class UserCondition(models.Model):
    UserConditionID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    ConditionID = models.ForeignKey(Condition, on_delete=models.CASCADE)
    Timestamp = models.DateTimeField(auto_now_add=True)

class UserTestHistory(models.Model):
    TestHistoryID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    TestName = models.CharField(max_length=100)
    TestDate = models.DateField()
    TestResult = models.CharField(max_length=100)
    LabName = models.CharField(max_length=100)
    DoctorName = models.CharField(max_length=100)
    Notes = models.TextField()

class UserConsultationHistory(models.Model):
    ConsultationID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    DoctorName = models.CharField(max_length=100)
    ConsultationDate = models.DateTimeField(auto_now_add=True)
    Diagnosis = models.TextField()
    TreatmentPlan = models.TextField()
    Notes = models.TextField()

class SymptomManager(models.Manager):
    def get_all_symptoms(self):
        return self.all()

    def get_symptom_by_id(self, SymptomId):
        return self.get(id=SymptomId)

    def record_user_symptom(self, UserId, SymptomId, Severity):
        try:
            User = User.objects.get(pk=UserId)
            Symptom = Symptom.objects.get(pk=SymptomId)
            ExistingRecord = UserSymptom.objects.filter(User=User, Symptom=Symptom).first()

            if ExistingRecord:
                ExistingRecord.Severity = Severity
                ExistingRecord.save()
            else:
                UserSymptom.objects.create(User=User, Symptom=Symptom, Severity=Severity)

            return "Symptom recorded successfully"
        except User.DoesNotExist:
            return "User not found"
        except Symptom.DoesNotExist:
            return "Symptom not found"
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "An unexpected error occurred. Please try again or contact support."