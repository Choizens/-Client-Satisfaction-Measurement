from django.shortcuts import render, redirect
from django.db.models import Avg
from django.contrib import messages
from .models import SatisfactionSurvey, Pin


def code(request):
    # landing page after submission
    return render(request, "Code.html")


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

    return render(request, "page1.html", request.session.get('page1', {}))


def page2(request):
    if request.method == "POST":
        if "back" in request.POST:
            return redirect("page1")

        # CC1 → allow up to 3 selections
        cc1_vals = request.POST.getlist("cc1")
        if len(cc1_vals) > 3:
            cc1_vals = cc1_vals[:3]

        # CC2 & CC3 → allow only one
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

    return render(request, "page2.html", request.session.get('page2', {}))

def page3(request):
    if request.method == "POST":
        if "back" in request.POST:
            return redirect("page2")

        # Collect ratings
        ratings = {}
        for i in range(9):
            ratings[f"sod{i}"] = int(request.POST.get(f"sod{i}", 6))  # default N/A=6

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
        page3 = request.session.get("page3", {})

        survey = SatisfactionSurvey.objects.create(
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

            sod0=page3.get("sod0"),
            sod1=page3.get("sod1"),
            sod2=page3.get("sod2"),
            sod3=page3.get("sod3"),
            sod4=page3.get("sod4"),
            sod5=page3.get("sod5"),
            sod6=page3.get("sod6"),
            sod7=page3.get("sod7"),
            sod8=page3.get("sod8"),

            feedback=page3.get("feedback"),
            email=page3.get("email"),
        )

        # clear session for new user
        for key in ['page1', 'page2', 'page3']:
            request.session.pop(key, None)

        return redirect("Code")

    return render(request, "page3.html", request.session.get('page3', {}))


def dashboard(request):
    surveys = SatisfactionSurvey.objects.all()
    total_surveys = surveys.count()
    active_surveys = total_surveys  # you can adjust logic if some surveys are inactive
    total_responses = surveys.count()
    satisfaction_rate = surveys.aggregate(avg=Avg('sod4'))['avg'] or 0  # example: using sod4 as satisfaction

    return render(request, "Dashboard.html", {
        "surveys": surveys,
        "total_surveys": total_surveys,
        "active_surveys": active_surveys,
        "total_responses": total_responses,
        "satisfaction_rate": round(satisfaction_rate, 2),
    })

def code(request):
    if request.method == "POST":
        code_input = request.POST.get("code")

        if Pin.objects.filter(code=code_input).exists():
            return redirect("page1") 
        else:
            messages.error(request, "PIN does not exist.")
            return redirect("Code") 

    return render(request, "Code.html") 