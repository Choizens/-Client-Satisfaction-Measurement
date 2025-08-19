from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import SatisfactionSurvey


def code(request):
    # Landing page after survey done
    return render(request, 'Code.html')

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
        return redirect('page2')

    context = request.session.get('page1', {})
    return render(request, 'page1.html', context)


def page2(request):
    if request.method == "POST":
        if 'back' in request.POST:
            return redirect('page1')

        # cc1 multiple (store up to 3)
        cc1_values = request.POST.getlist("cc1")
        if len(cc1_values) > 3:
            cc1_values = cc1_values[:3]  # enforce max 3

        request.session['page2'] = {
            'cc1': cc1_values,
            'cc2': request.POST.get("cc2"),
            'cc3': request.POST.get("cc3"),
        }
        return redirect('page3')

    context = request.session.get('page2', {})
    return render(request, 'page2.html', context)


def page3(request):
    if request.method == "POST":
        if 'back' in request.POST:
            return redirect('page2')

        # collect ratings (0–8)
        ratings = {}
        for i in range(9):
            ratings[f"sod{i}"] = int(request.POST.get(f"sod{i}", 6))  # default N/A=6

        # save in session
        request.session['page3'] = {
            'ratings': ratings,
            'feedback': request.POST.get("feedback"),
            'email': request.POST.get("email"),
        }

        # ✅ Save everything in DB only on Done
        page1 = request.session.get('page1', {})
        page2 = request.session.get('page2', {})
        page3 = request.session.get('page3', {})

        if page1 and page2 and page3:
            survey = SatisfactionSurvey.objects.create(
                clientType=page1.get('clientType'),
                government=page1.get('government'),
                visitDate=page1.get('visitDate'),
                sex=page1.get('sex'),
                age=page1.get('age'),
                region=page1.get('region'),
                officePerson=page1.get('officePerson'),
                serviceAvailed=page1.get('serviceAvailed'),
                cc1=",".join(page2.get('cc1', [])),
                cc2=page2.get('cc2'),
                cc3=page2.get('cc3'),
                sod0=page3['ratings'].get("sod0", 6),
                sod1=page3['ratings'].get("sod1", 6),
                sod2=page3['ratings'].get("sod2", 6),
                sod3=page3['ratings'].get("sod3", 6),
                sod4=page3['ratings'].get("sod4", 6),
                sod5=page3['ratings'].get("sod5", 6),
                sod6=page3['ratings'].get("sod6", 6),
                sod7=page3['ratings'].get("sod7", 6),
                sod8=page3['ratings'].get("sod8", 6),
                feedback=page3.get('feedback'),
                email=page3.get('email'),
            )

            # Clear session for new user
            for key in ['page1', 'page2', 'page3']:
                if key in request.session:
                    del request.session[key]

            return redirect('Code')

    context = request.session.get('page3', {})
    return render(request, 'page3.html', context)

def dashboard(request):
    return render(request, 'Dashboard.html')
