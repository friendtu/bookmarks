from django.shortcuts import render,redirect
from .forms import ImageCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def image_create(request):
    if request.method=='POST':
        cd=form.clean_data
        new_item=form.save(commit=False)
        new_item.user=request.user
        new_item.save()
        message.success(request,"Image added successfully")
        return redirect(new_item.get_absolute_url())
    else:
        form=ImageCreateForm(data=request.GET)
    return render(request,'images/image/create.html',{
        'section':'images',
        'form':form
        })