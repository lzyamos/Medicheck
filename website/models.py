from django.db import models
import logging

logger = logging.getLogger(__name__)

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50, unique=True)
    Password = models.CharField(max_length=100)
    Email = models.CharField(max_length=100, unique=True)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    RegistrationDate = models.DateTimeField(auto_now_add=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.Username

class Record(models.Model):
    RecordID = models.CharField(primary_key=True, max_length=10, default="100001")
    Created_at = models.DateTimeField(auto_now_add=True)
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Email = models.CharField(max_length=100)
    Phone = models.CharField(max_length=15, default="2457000000000")

    def __str__(self):
        return f"{self.First_name} {self.Last_name}"

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
    Notes = models.TextField()

class SymptomManager(models.Manager):
    def get_all_symptoms(self):
        return self.all()

    def get_symptom_by_id(self, SymptomId):
        return self.get(id=SymptomId)

    def record_user_symptom(self, UserId, SymptomId, Severity):
        try:
            UserObj = User.objects.get(pk=UserId)
            SymptomObj = Symptom.objects.get(pk=SymptomId)
            ExistingRecord = UserSymptom.objects.filter(User=UserObj, Symptom=SymptomObj).first()

            if ExistingRecord:
                ExistingRecord.Severity = Severity
                ExistingRecord.save()
            else:
                UserSymptom.objects.create(User=UserObj, Symptom=SymptomObj, Severity=Severity)

            return "Symptom recorded successfully"
        except User.DoesNotExist:
            logger.error("User not found")
            return "User not found"
        except Symptom.DoesNotExist:
            logger.error("Symptom not found")
            return "Symptom not found"
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return "An unexpected error occurred. Please try again or contact support."

class ConditionManager(models.Manager):
    def get_all_conditions(self):
        return self.all()

    def get_condition_by_id(self, condition_id):
        return self.get(id=condition_id)

    def suggest_condition_to_user(self, user_id, condition_id):
        try:
            user = User.objects.get(pk=user_id)
            condition = Condition.objects.get(pk=condition_id)

            UserCondition.objects.create(User=user, Condition=condition)

            return "Condition suggested to user successfully"
        except User.DoesNotExist:
            logger.error("User not found")
            return "User not found"
        except Condition.DoesNotExist:
            logger.error("Condition not found")
            return "Condition not found"
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return "An unexpected error occurred. Please try again or contact support."
