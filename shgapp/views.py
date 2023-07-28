from django.shortcuts import render, redirect

# view for the home page 

def home(request):
    return render(request, 'home.html')


#view for the branch details
from .forms import BranchDetailsForm
from .models import BranchDetails
def create_branch_view(request):
    if request.method == 'POST':
        form = BranchDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Branch details saved successfully.')
            return redirect('create_branch')  # Redirect to a success page or branch list
    else:
        form = BranchDetailsForm()
        message_list = [str(message) for message in messages.get_messages(request)]
    
    branches = BranchDetails.objects.all()
    return render(request, 'create_branch.html', {'form': form, 'branches': branches,'messages': message_list})


def update_branch_view(request, branch_id):
    branch = BranchDetails.objects.get(id=branch_id)
    if request.method == 'POST':
        form = BranchDetailsForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Branch details updated successfully.')
            return redirect('create_branch')  # Redirect to a success page or branch list
    else:
        form = BranchDetailsForm(instance=branch)
        message_list = [str(message) for message in messages.get_messages(request)]
    
    return render(request, 'update_branch.html', {'form': form, 'branch': branch ,'messages': message_list})

#------------------------------------------------------------------------------------------------------------------------------
#view for the society details
from .forms import SocietyDetailsForm
from .models import SocietyDetails
from django.contrib import messages

def create_society_view(request):
    if request.method == 'POST':
        form = SocietyDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Society details saved successfully.')
            return redirect('create_society_view')
    else:
        form = SocietyDetailsForm()
        message_list = [str(message) for message in messages.get_messages(request)]
    
    society = SocietyDetails.objects.all()
    return render(request, 'create_society.html', {'form': form, 'society': society, 'messages': message_list})

def update_society_view(request, soc_id):
    society = SocietyDetails.objects.get(id=soc_id)
    if request.method == 'POST':
        form = SocietyDetailsForm(request.POST, instance=society)
        if form.is_valid():
            form.save()
            messages.success(request, 'Society details updated successfully.')
            return redirect('create_society_view')

    else:
        form = SocietyDetailsForm(instance=society)
        message_list = [str(message) for message in messages.get_messages(request)]
        

    return render(request, 'update_society.html', {'form': form, 'society': society, 'messages': message_list})



import pandas as pd
from django.shortcuts import render
from .models import SocietyDetails

def upload_file_society(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']

        # Assuming the first row in the Excel file contains column headers
        df = pd.read_excel(excel_file)

        # Iterate through each row in the DataFrame and save the data to the database
        for index, row in df.iterrows():
            society_code = row['society_code']
            society_name = row['society_name']
            branch_name = row['branch_name']
            taluka = row['taluka']
            district = row['district']

            SocietyDetails.objects.create(
                society_code=society_code,
                society_name=society_name,
                branch_name=branch_name,
                taluka=taluka,
                district=district
            )

        return render(request, 'upload_success.html')
    
    return render(request, 'upload_form_society.html')

        
#--------------------------------------------------------------------------------------------------------------------

# views.py code for shg bank details 
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SHGDetailsForm
from .models import shgdetails

def shg_details_bank_form(request):
    if request.method == 'POST':
        form = SHGDetailsForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            
            if shgdetails.objects.filter(group_name=group_name).exists():
                messages.error(request, 'Group name already exists. Please enter a different name.')
                form.add_error('group_name', 'Group name already exists.')
            else:
                shg = form.save(commit=False)
                
                latest_group = shgdetails.objects.only('group_no').order_by('-group_no').first()
                group_no = latest_group.group_no + 1 if latest_group else 1
                
                shg.group_no = group_no
                shg.sycode = 0
                shg.society_name = 'None'
                shg.save()
                messages.success(request, 'Form submitted successfully!')
                return redirect('shg_details_form')
    else:
        latest_group = shgdetails.objects.only('group_no').order_by('-group_no').first()
        group_no = latest_group.group_no + 1 if latest_group else 1
        
        initial_data = {'group_no': group_no}
        form = SHGDetailsForm(initial=initial_data)
    
    context = {'form': form}
    return render(request, 'shg_details_bank_form.html', context)



from django.http import JsonResponse
from .models import shgdetails

def get_group_bank_names(request):
    search_query = request.GET.get('search_query', '')

    matched_group_names = (
        shgdetails.objects.filter(group_name__icontains=search_query)
        .values_list('group_name', flat=True)
        .distinct()
    )
    
    response_data = {'suggestions': list(matched_group_names)}
    return JsonResponse(response_data)


#-------------------------------------------------------------------------------------------------------------------------
#view code for the shg society details 
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SHGDetailssocietyForm
from .models import shgdetails, SocietyDetails



def shg_details_society_form(request):
    if request.method == 'POST':
        form = SHGDetailssocietyForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            society_name = form.cleaned_data['societyname']
            
            if shgdetails.objects.filter(group_name=group_name).exists():
                messages.error(request, 'Group name already exists. Please enter a different name.')
                form.add_error('group_name', 'Group name already exists.')
            else:
                shg = form.save(commit=False)
                # Get the selected society_name from the form
                selected_society_name = form.cleaned_data['societyname']
                
                # Get the corresponding society_code from the SocietyDetails model
                try:
                    society_details = SocietyDetails.objects.get(society_name=selected_society_name)
                    society_code = society_details.society_code
                    shg.sycode = society_code  # Set the society_code in shgdetails
                except SocietyDetails.DoesNotExist:
                    messages.error(request, 'Selected society does not exist in the database.')
                    form.add_error('societyname', 'Selected society does not exist.')
                    return render(request, 'shg_details_soceity_form.html', {'form': form})
                
                latest_group = shgdetails.objects.only('group_no').order_by('-group_no').first()
                group_no = latest_group.group_no + 1 if latest_group else 1
                
                shg.group_no = group_no
                shg.society_name = society_name

                shg.branchname = 'None'
                shg.save()
                messages.success(request, 'Form submitted successfully!')
                return redirect('shg_details_society_form')
    else:
        latest_group = shgdetails.objects.only('group_no').order_by('-group_no').first()
        group_no = latest_group.group_no + 1 if latest_group else 1
        
        initial_data = {'group_no': group_no}
        form = SHGDetailssocietyForm(initial=initial_data)
    
    context = {'form': form}
    return render(request, 'shg_details_soceity_form.html', context)


from django.http import JsonResponse
from .models import shgdetails

def get_group_society_names(request):
    search_query = request.GET.get('search_query', '')

    matched_group_names = (
        shgdetails.objects.filter(group_name__icontains=search_query)
        .values_list('group_name', flat=True)
        .distinct()
    )
    
    response_data = {'suggestions': list(matched_group_names)}
    return JsonResponse(response_data)



#----------------------------------------------------------------------------------------------------------------------------------------

from django.shortcuts import render, HttpResponse
import json
from .models import shgdetails
from .forms import SHGTransactionForm

def create_shgtransaction_bank(request):
    if request.method == 'POST':
        form = SHGTransactionForm(request.POST)
        if form.is_valid():
            # Set the group_no based on the selected group_name

            group_name = form.cleaned_data['group_name']
            group_no = shgdetails.objects.get(group_name=group_name).group_no
            form.instance.group_no = group_no

            form.instance.branchname = form.cleaned_data['branchname']

            # Set sycode to 0 and society_name to 'None'
            form.instance.sycode = 0
            form.instance.society_name = 'None'

            form.save()
            # Add any additional processing if needed
        else:
            # If the form is not valid, print the errors to the console
            print(form.errors)
    else:
        form = SHGTransactionForm()

    context = {'form': form}
    return render(request, 'sample.html', context)



def get_group_names_bank(request, branchname):
    group_names = shgdetails.objects.filter(branchname=branchname).values_list('group_name', flat=True)
    return HttpResponse(json.dumps(list(group_names)), content_type='application/json')

#---------------------------------------------------------------------------------------------------------------------------------


from django.shortcuts import render, HttpResponse
import json
from .models import shgdetails
from .forms import shgtrnasactionsocietyform

def create_shgtransaction_society(request):
    if request.method == 'POST':
        form = shgtrnasactionsocietyform(request.POST)
        if form.is_valid():
            # Set the group_no based on the selected group_name

            group_name = form.cleaned_data['group_name']
            group_no = shgdetails.objects.get(group_name=group_name).group_no
            form.instance.group_no = group_no

            form.instance.society_name = form.cleaned_data['society_name']
            syname = form.cleaned_data['society_name']
            sycode = shgdetails.objects.get(society_name=syname).sycode
            form.instance.sycode = sycode

            form.instance.branchname = 'None'

            form.save()
            # Add any additional processing if needed
        else:
            # If the form is not valid, print the errors to the console
            print(form.errors)
    else:
        form = shgtrnasactionsocietyform()

    context = {'form': form}
    return render(request, 'sample123.html', context)



def get_group_names_society(request, society_name):
    group_names = shgdetails.objects.filter(society_name=society_name).values_list('group_name', flat=True)
    return HttpResponse(json.dumps(list(group_names)), content_type='application/json')



    


    






