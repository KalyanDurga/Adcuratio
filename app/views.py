from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect 
# Create your views here.
from django.core.mail import send_mail
from app.forms import *

from django.contrib.auth import authenticate,login,logout
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ViewSet
from app.serializers import *
from django.views.generic import CreateView


from rest_framework.response import Response

def home(request):

    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    

    return render(request,'home.html')



def registration(request):
    ufo=Userform()
    d={'ufo':ufo}

    if request.method=='POST':
        ufd=Userform(request.POST)
        if ufd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()

            send_mail('Registratioon',
                      "Succefully Registration is Done",
                      'kalyandurga002@gmail.com',
                      [NSUO.email],
                      fail_silently=False

                      )


            return HttpResponse('Regsitration is Susssessfulll')
        else:
            return HttpResponse('Not valid')

    return render(request,'registration.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password') 
        
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
    
@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)

class TravelData(ViewSet):
    def list(self,request):
        ADO=Travel.objects.all()
        SJD=TravelSeriallizer(ADO,many=True)
        d={'data':SJD.data}
        return render(request,'list.html',d)

    def retrieve(self,request,pk):
        TO=Travel.objects.get(pk=pk)
        SDO=TravelSeriallizer(TO)
        return Response(SDO.data)
        

    def update(self,request,pk):
        SPO=Travel.objects.get(pk=pk)
        SPD=TravelSeriallizer(SPO,data=request.data)
        if SPD.is_valid():
            SPD.save()
            return Response({'Updated':'Travel is updated'})
        else:
            return Response({'Failed':'Travel is Not Updated'})
    
    def partial_update(self,request,pk):
        SPO=Travel.objects.get(pk=pk)
        SPD=TravelSeriallizer(SPO,data=request.data,partial=True)
        if SPD.is_valid():
            SPD.save()
            return Response({'Updated':'Travel is updated'})
        else:
            return Response({'Failed':'Travel is Not Updated'})
    def destroy(self,request,pk):
        Travel.objects.get(pk=pk).delete()
        return Response({'Deleted':'Travel is deleted'})
    

    
    
class CreateTravel(CreateView):
    template_name='travel.html'
    form_class=TravelForm

    def form_valid(self,form):
        form.save()
        return HttpResponseRedirect(reverse('home'))






















