from django.db import models

class SatisfactionSurvey(models.Model):
    # Page1
    clientType = models.CharField(max_length=100)
    government = models.CharField(max_length=100)
    visitDate = models.DateField()
    sex = models.CharField(max_length=20)
    age = models.IntegerField()
    region = models.CharField(max_length=200)
    officePerson = models.CharField(max_length=200)
    serviceAvailed = models.TextField()

    # Page2
    cc1 = models.CharField(max_length=200)  # store as comma-separated
    cc2 = models.CharField(max_length=10)
    cc3 = models.CharField(max_length=10)

    # Page3 ratings (SOD0–SOD8)
    sod0 = models.IntegerField()
    sod1 = models.IntegerField()
    sod2 = models.IntegerField()
    sod3 = models.IntegerField()
    sod4 = models.IntegerField()
    sod5 = models.IntegerField()
    sod6 = models.IntegerField()
    sod7 = models.IntegerField()
    sod8 = models.IntegerField()

    feedback = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Survey by {self.clientType} on {self.visitDate}"