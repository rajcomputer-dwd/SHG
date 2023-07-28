from django import forms

#class for the branch details
from .models import BranchDetails
class BranchDetailsForm(forms.ModelForm):
    class Meta:
        model = BranchDetails
        fields = '__all__'  # Include all fields from the model

#class for the society details
from .models import SocietyDetails
class SocietyDetailsForm(forms.ModelForm):
    class Meta:
        model = SocietyDetails
        fields = '__all__'



#class for the shg details with Bank 
from django import forms
from .models import shgdetails, BranchDetails

class SHGDetailsForm(forms.ModelForm):
    branchname = forms.ModelChoiceField(queryset=BranchDetails.objects.all(), empty_label=None)
    
    class Meta:
        model = shgdetails
        exclude = ['sycode', 'society_name']
        widgets = {
            'group_no': forms.TextInput(attrs={'readonly': True}),
        }

#class for the shg details with society 
from django import forms
from .models import shgdetails, SocietyDetails

class SHGDetailssocietyForm(forms.ModelForm):
    societyname = forms.ModelChoiceField(queryset=SocietyDetails.objects.all(), empty_label=None)
    class Meta:
        model = shgdetails
        exclude = ['branchname', 'sycode', 'society_name']  # Exclude the 'branchname' field from the form
        widgets = {
            'group_no': forms.TextInput(attrs={'readonly': True}),
           
        }



#form for the shg transaction branch
from django import forms
from django.db.models import OuterRef, Subquery
from .models import shgtransaction, BranchDetails, shgdetails

class SHGTransactionForm(forms.ModelForm):
    branchname = forms.ModelChoiceField(
        queryset=BranchDetails.objects.values_list('branchname', flat=True).distinct(),
        empty_label=None,
        required=True,
        to_field_name='branchname',
    )
    group_name = forms.ChoiceField(choices=(), required=False)

    class Meta:
        model = shgtransaction
        fields = '__all__'
        exclude = ['sycode', 'society_name', 'group_no', 'branchname']

    def __init__(self, *args, **kwargs):
        super(SHGTransactionForm, self).__init__(*args, **kwargs)
        if 'branchname' in self.data:
            self.fields['group_name'].choices = self.get_group_names()

    def get_group_names(self):
        branchname = self.data['branchname']
        groups = shgdetails.objects.filter(branchname=branchname).values_list('group_name', flat=True).exclude(group_name=None)
        return [(group, group) for group in groups]


#form for the shg transaction society
from .models import shgtransaction, SocietyDetails, shgdetails

class shgtrnasactionsocietyform(forms.ModelForm):
    society_name = forms.ModelChoiceField(
        queryset=SocietyDetails.objects.values_list('society_name', flat=True).distinct(),
        empty_label=None,
        required=True,
        to_field_name='society_name',
    )
    group_name = forms.ChoiceField(choices=(), required=False)

    class Meta:
        model = shgtransaction
        fields = '__all__'
        exclude = ['sycode', 'society_name', 'group_no', 'branchname']
    
    def __init__(self, *args, **kwargs):
        super(shgtrnasactionsocietyform, self).__init__(*args, **kwargs)
        if 'society_name' in self.data:
            self.fields['group_name'].choices = self.get_group_names_society()

    def get_group_names_society(self):
        society_name = self.data['society_name']
        groups = shgdetails.objects.filter(society_name=society_name).values_list('group_name', flat=True).exclude(group_name=None)
        return [(group, group) for group in groups]


    

