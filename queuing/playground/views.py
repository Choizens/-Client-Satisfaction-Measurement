from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.core.serializers.json import DjangoJSONEncoder
import json

# ✅ Import your app models
from .models import (
    SatisfactionSurvey,
    Pin,
    Survey1,
    Survey2,
    Survey3,
    Survey3Question,
)


def page1(request):
    if request.method == "POST":
        request.session['page1'] = {
            'clientType': request.POST.get("clientType"),
            'government': request.POST.get("government"),
            'visitDate': request.POST.get("visitDate"),
            'sex': request.POST.get("sex"),
            'age': request.POST.get("age"),
            'region': request.POST.get("region"),
            'officePerson': request.POST.get("officePerson"),
            'serviceAvailed': request.POST.get("serviceAvailed"),
        }
        return redirect("page2")

    # Fetch survey config (always use first record)
    survey = Survey1.objects.first()

    return render(
        request,
        "Survey/page1.html",
        {
            "form_data": request.session.get('page1', {}),
            "survey": survey
        }
    )

def msurvey1(request):
    surveys = Survey1.objects.all()
    
    # Example form_data dict
    form_data = request.POST if request.method == "POST" else {}

    # Preprocess each field explicitly
    context = {
        "surveys": surveys,
        "clientType": form_data.get("clientType", ""),
        "government": form_data.get("government", ""),
        "visitDate": form_data.get("visitDate", ""),
        "sex": form_data.get("sex", ""),
        "age": form_data.get("age", ""),
        "region": form_data.get("region", ""),
        "officePerson": form_data.get("officePerson", ""),
        "serviceAvailed": form_data.get("serviceAvailed", ""),
    }
    return render(request, "managesur/msurvey1.html", context)




























    
def page2(request):
    if request.method == "POST":
        if "back" in request.POST:
            # save current answers before going back
            request.session['page2'] = {
                'cc1': request.POST.getlist("cc1"),
                'cc2': request.POST.get("cc2"),
                'cc3': request.POST.get("cc3"),
            }
            return redirect("page1")

        # CC1 → allow up to 3 selections
        cc1_vals = request.POST.getlist("cc1")
        if len(cc1_vals) > 3:
            cc1_vals = cc1_vals[:3]

        cc2_vals = request.POST.getlist("cc2")
        cc2_val = cc2_vals[0] if cc2_vals else None

        cc3_vals = request.POST.getlist("cc3")
        cc3_val = cc3_vals[0] if cc3_vals else None

        request.session['page2'] = {
            'cc1': cc1_vals,
            'cc2': cc2_val,
            'cc3': cc3_val,
        }
        return redirect("page3")

    # ✅ Fetch the survey text (use first record)
    survey2 = Survey2.objects.first()

    context = request.session.get('page2', {})
    context['survey2'] = survey2   # pass to template

    return render(request, "Survey/page2.html", context)




def page3(request):
    # fetch text data
    survey_text = Survey3.objects.first()
    if not survey_text:
        survey_text = Survey3.objects.create()

    # prepare saved ratings for template
    saved_ratings = request.session.get("page3", {})

    if request.method == "POST":
        if "back" in request.POST:
            ratings = {}
            for i, q in enumerate(survey_text.get_questions()):
                ratings[f"sod{i}"] = request.POST.get(f"sod{i}") or "0"

            feedback = request.POST.get("feedback")
            email = request.POST.get("email")

            request.session['page3'] = {
                **ratings,
                "feedback": feedback,
                "email": email,
            }
            return redirect("page2")

        # Collect ratings for submit
        ratings = {}
        for i, q in enumerate(survey_text.get_questions()):
            ratings[f"sod{i}"] = request.POST.get(f"sod{i}") or "0"

        feedback = request.POST.get("feedback")
        email = request.POST.get("email")

        request.session['page3'] = {
            **ratings,
            "feedback": feedback,
            "email": email,
        }

        # save all to DB
        page1 = request.session.get("page1", {})
        page2 = request.session.get("page2", {})
        page3_data = request.session.get("page3", {})

        SatisfactionSurvey.objects.create(
            clientType=page1.get("clientType"),
            government=page1.get("government"),
            visitDate=page1.get("visitDate"),
            sex=page1.get("sex"),
            age=page1.get("age"),
            region=page1.get("region"),
            officePerson=page1.get("officePerson"),
            serviceAvailed=page1.get("serviceAvailed"),

            cc1=",".join(page2.get("cc1", [])),
            cc2=page2.get("cc2"),
            cc3=page2.get("cc3"),

            **{f"sod{i}": page3_data.get(f"sod{i}", "0") for i in range(len(survey_text.get_questions()))},

            feedback=page3_data.get("feedback"),
            email=page3_data.get("email"),
        )

        for key in ['page1', 'page2', 'page3']:
            request.session.pop(key, None)

        return redirect("Code")

    return render(request, "Survey/page3.html", {
        "survey_text": survey_text,
        "questions": survey_text.get_questions(),
        "savedRatings": saved_ratings,  # ✅ pass dictionary directly
        "feedback": saved_ratings.get("feedback", ""),
        "email": saved_ratings.get("email", ""),
    })




def dashboard(request):

    surveys = SatisfactionSurvey.objects.all().order_by('-submitted_at')
    

    total_surveys = surveys.count()
    total_responses = surveys.count()
    

    satisfaction_fields = ['sod0', 'sod1', 'sod2', 'sod3', 'sod4', 'sod5', 'sod6', 'sod7', 'sod8']
    satisfaction_rate = 0
    if surveys.exists():
        total_ratings = 0
        sum_ratings = 0
        for survey in surveys:
            for field in satisfaction_fields:
                rating = getattr(survey, field)
                if rating:
                    total_ratings += 1
                    sum_ratings += rating
        if total_ratings > 0:
            
            avg_rating = sum_ratings / total_ratings
            satisfaction_rate = ((avg_rating - 1) / 4) * 100 
    
    # Gender distribution
    male_count = surveys.filter(sex__iexact='male').count()
    female_count = surveys.filter(sex__iexact='female').count()
    

    strongly_agree = 0
    agree = 0
    neutral = 0
    disagree = 0
    strongly_disagree = 0
    not_applicable = 0
    
    for survey in surveys:
        for field in satisfaction_fields:
            rating = getattr(survey, field)
            if rating == 5:
                strongly_agree += 1
            elif rating == 4:
                agree += 1
            elif rating == 3:
                neutral += 1
            elif rating == 2:
                disagree += 1
            elif rating == 1:
                strongly_disagree += 1
            else:
                not_applicable += 1
    
    # CC Analysis - Calculate distributions
    cc1_counts = [0, 0, 0, 0] 
    cc2_counts = [0, 0, 0, 0, 0]  
    cc3_counts = [0, 0, 0, 0]  
    
    for survey in surveys:
 
        if survey.cc1:
            try:
                selected_options = survey.cc1.split(',')
                for option in selected_options:
                    option_num = int(option.strip())
                    if 1 <= option_num <= 4:
                        cc1_counts[option_num-1] += 1
            except (ValueError, AttributeError):
                pass
        

        if survey.cc2:
            try:
                option_num = int(survey.cc2)
                if 1 <= option_num <= 5:
                    cc2_counts[option_num-1] += 1
            except (ValueError, AttributeError):
                pass
        

        if survey.cc3:
            try:
                option_num = int(survey.cc3)
                if 1 <= option_num <= 4:
                    cc3_counts[option_num-1] += 1
            except (ValueError, AttributeError):
                pass
    

    paginator = Paginator(surveys, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'surveys': surveys,
        'page_obj': page_obj,
        'total_surveys': total_surveys,
        'total_responses': total_responses,
        'satisfaction_rate': round(satisfaction_rate, 1),
        'male_count': male_count,
        'female_count': female_count,
        'strongly_agree': strongly_agree,
        'agree': agree,
        'neutral': neutral,
        'disagree': disagree,
        'strongly_disagree': strongly_disagree,
        'not_applicable': not_applicable,
        # CC Analysis data
        'cc1_option1': cc1_counts[0],
        'cc1_option2': cc1_counts[1], 
        'cc1_option3': cc1_counts[2],
        'cc1_option4': cc1_counts[3],
        'cc2_option1': cc2_counts[0],
        'cc2_option2': cc2_counts[1],
        'cc2_option3': cc2_counts[2], 
        'cc2_option4': cc2_counts[3],
        'cc2_option5': cc2_counts[4],
        'cc3_option1': cc3_counts[0],
        'cc3_option2': cc3_counts[1],
        'cc3_option3': cc3_counts[2],
        'cc3_option4': cc3_counts[3]
    }
    
    return render(request, 'Survey/Dashboard.html', context)



def code(request):
    if request.method == "POST":
        code_input = request.POST.get("code")

        if Pin.objects.filter(code=code_input).exists():
            return redirect("page1") 
        else:
            messages.error(request, "PIN does not exist.")
            return redirect("Code") 

    return render(request, "Survey/Code.html") 




# Manage Surveys

def manage_survey(request):
    return render(request, "Survey/manage.html")


# locations

def msurvey1(request):
    return render(request, "managesur/msurvey1.html")

def msurvey2(request):
    return render(request, "managesur/msurvey2.html")

def msurvey3(request):
    return render(request, "managesur/msurvey3.html")