from django.db import models

class SatisfactionSurvey(models.Model):
    # Page1 fields
    clientType = models.CharField(max_length=50)
    government = models.CharField(max_length=50)
    visitDate = models.DateField()
    sex = models.CharField(max_length=20)
    age = models.IntegerField()
    region = models.CharField(max_length=100)
    officePerson = models.CharField(max_length=100)
    serviceAvailed = models.TextField()

    # Page2 fields
    cc1 = models.CharField(max_length=200)   # stored as comma-separated (max 3)
    cc2 = models.CharField(max_length=5)
    cc3 = models.CharField(max_length=5)

    # Page3 ratings
    sod0 = models.IntegerField()
    sod1 = models.IntegerField()
    sod2 = models.IntegerField()
    sod3 = models.IntegerField()
    sod4 = models.IntegerField()
    sod5 = models.IntegerField()
    sod6 = models.IntegerField()
    sod7 = models.IntegerField()
    sod8 = models.IntegerField()

    # Feedback + email
    feedback = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Survey {self.id} - {self.clientType}"
    

class Pin(models.Model):
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.code


class Survey1(models.Model):
    # Intro/Instruction Section
    intro_title = models.CharField(
        max_length=255,
        default="Client Satisfaction Measurement (CSM)"
    )
    intro_desc1 = models.TextField(
        default="The Client Satisfaction Measurement (CSM) tracks the customer experience of government offices. Your feedback on your recently concluded transaction will help this office provide a better service."
    )
    intro_desc2 = models.TextField(
        default="Personal information shared will be kept confidential and you always have the option to not answer this form."
    )
    transaction_type = models.CharField(
        max_length=255,
        default="recently concluded transaction"
    )

    # Row 1
    client_type_label = models.CharField(max_length=255, default="Client type:")
    client_type_options = models.JSONField(
        default=list,
        help_text="Example: [\"Student Applicant\", \"Citizen (Student/Parents/Alumni)\", \"Business\"]"
    )

    government_label = models.CharField(max_length=255, default="Government:")
    government_options = models.JSONField(
        default=list,
        help_text="Example: [\"Employee\", \"Other Agency\"]"
    )

    visit_date_label = models.CharField(max_length=255, default="Date:")

    # Row 2
    sex_label = models.CharField(max_length=255, default="Sex:")
    sex_options = models.JSONField(
        default=list,
        help_text="Example: [\"Male\", \"Female\", \"Others\"]"
    )

    age_label = models.CharField(max_length=255, default="Age:")

    # Row 3
    region_label = models.CharField(max_length=255, default="Region of Residence:")
    office_person_label = models.CharField(max_length=255, default="Office Person Visited:")

    # Row 4
    service_availed_label = models.CharField(max_length=255, default="Service Availed:")

    # Submit Button
    submit_text = models.CharField(max_length=255, default="NEXT")

    def __str__(self):
        return f"Survey1 - {self.intro_title}"


class Survey2(models.Model):
    # Store the instruction text
    instruction = models.TextField(
        default="Please Check(✓) your answer to the Citizen's Charter (CC) questions. "
                "The Citizen's Charter is an official document that reflects the services "
                "of a government agency including its requirements, fees, and processing time among others."
    )

    # CC1
    cc1_code = models.CharField(max_length=10, default="CC1")
    cc1_question = models.TextField(default="Which of the following best describes your awareness of a CC?")
    cc1_option1 = models.CharField(max_length=255, default="I know what a CC is and I saw this office's CC.")
    cc1_option2 = models.CharField(max_length=255, default="I know what CC is but I did NOT see this office's CC.")
    cc1_option3 = models.CharField(max_length=255, default="I learned of the CC only when I saw this office's CC.")
    cc1_option4 = models.CharField(
        max_length=255,
        default="I do not know what a CC is and I did not see one in the office (Answer 'N/A' on CC2 and CC3)"
    )

    # CC2
    cc2_code = models.CharField(max_length=10, default="CC2")
    cc2_question = models.TextField(default="If aware of the CC (answered 1-3 in CC1), would you say that the CC of this office was ...?")
    cc2_option1 = models.CharField(max_length=255, default="Easy to see")
    cc2_option2 = models.CharField(max_length=255, default="Somewhat easy to see")
    cc2_option3 = models.CharField(max_length=255, default="Difficult to see")
    cc2_option4 = models.CharField(max_length=255, default="Not visible at all")
    cc2_option5 = models.CharField(max_length=255, default="N/A")

    # CC3
    cc3_code = models.CharField(max_length=10, default="CC3")
    cc3_question = models.TextField(default="If aware of the CC (answered 1-3 in CC1), how much did the CC help you in your transaction?")
    cc3_option1 = models.CharField(max_length=255, default="Helped very much")
    cc3_option2 = models.CharField(max_length=255, default="Somewhat helped")
    cc3_option3 = models.CharField(max_length=255, default="Did not help")
    cc3_option4 = models.CharField(max_length=255, default="N/A")

    def __str__(self):
        return f"Survey2 - {self.id}"





class Survey3(models.Model):
    # General instructions
    instruction = models.TextField(default="For SOD 0-8, please click the star (★) on the row that best corresponds to your answer.")

    # Star legend
    stars_strongly_agree = models.CharField(max_length=255, default="Strongly Agree = ★★★★★")
    stars_agree = models.CharField(max_length=255, default="Agree = ★★★★")
    stars_neutral = models.CharField(max_length=255, default="Neither Agree nor Disagree = ★★★")
    stars_disagree = models.CharField(max_length=255, default="Disagree = ★★")
    stars_strongly_disagree = models.CharField(max_length=255, default="Strongly Disagree = ★")
    stars_na = models.CharField(max_length=255, default="N/A Not Applicable = Leave it blank")

    # Rating table headers
    rating_table_header1 = models.CharField(max_length=255, default="Service Quality Dimensions")
    rating_table_header2 = models.CharField(max_length=255, default="Rating")

    # Feedback section
    feedback_label = models.TextField(default="Suggestion on how we can further improve our services (optional):")

    # Email section
    email_label = models.CharField(max_length=255, default="Email address (Optional):")

    # SOD Questions (SOD0–SOD8)
    sod0 = models.TextField(default="I am satisfied with service that I availed")
    sod1 = models.TextField(default="I spent a reasonable amount of time for my transaction.")
    sod2 = models.TextField(default="The office followed the transaction's requirements and steps based on the information provided.")
    sod3 = models.TextField(default="The steps (including payment) I needed to do my transaction were easy and simple.")
    sod4 = models.TextField(default="I easily found information about my transaction from the office or its website.")
    sod5 = models.TextField(default="I paid a reasonable amount of fees for my transaction. (If service is free, mark N/A column)")
    sod6 = models.TextField(default="I feel the office was fair to everyone or 'walang palakasan' during my transaction.")
    sod7 = models.TextField(default="I was treated courteously by the staff, and (if asked for help) the staff was helpful.")
    sod8 = models.TextField(default="I got what I needed from the government office, or (if denied) denial of request was sufficiently explained to me.")

    def get_questions(self):
        return [
            {"code": "SOD0.", "text": self.sod0},
            {"code": "SOD1.", "text": self.sod1},
            {"code": "SOD2.", "text": self.sod2},
            {"code": "SOD3.", "text": self.sod3},
            {"code": "SOD4.", "text": self.sod4},
            {"code": "SOD5.", "text": self.sod5},
            {"code": "SOD6.", "text": self.sod6},
            {"code": "SOD7.", "text": self.sod7},
            {"code": "SOD8.", "text": self.sod8},
        ]

    def __str__(self):
        return "Survey3 Text Data"

class Survey3Question(models.Model):
    survey = models.ForeignKey(Survey3, on_delete=models.CASCADE, related_name="questions")
    code = models.CharField(max_length=10)   # e.g. "SOD0."
    text = models.TextField()                # question text

    def __str__(self):
        return f"{self.code} {self.text[:50]}"