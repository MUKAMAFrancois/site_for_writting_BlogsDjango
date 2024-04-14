from django import forms




class RegistrationForm(forms.Form):
    first_name=forms.CharField(max_length=100)
    last_name=forms.CharField(max_length=100)
    email=forms.EmailField(max_length=255)
    password=forms.CharField(max_length=255,widget=forms.PasswordInput)
    confirm_password=forms.CharField(max_length=255,widget=forms.PasswordInput)


class ProfileCreationForm(forms.Form):
    user_bio=forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'rows':5, 'cols':20}))
    phone_number=forms.CharField(max_length=15, required=False)
    wanna_be_a_blogger=forms.BooleanField(required=False,initial=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    user_company=forms.CharField(max_length=100, required=False)
    user_profile=forms.ImageField(required=False)



class LoginForm(forms.Form):
    email=forms.EmailField(max_length=255)
    password=forms.CharField(max_length=255,widget=forms.PasswordInput)


class ProfileUpdateForm(forms.Form):
    user_bio=forms.CharField(max_length=500, required=False,
                              widget=forms.Textarea(attrs={'rows':5, 'cols':20}))
    phone_number=forms.CharField(max_length=15, required=False)
    wanna_be_a_blogger=forms.BooleanField(required=False,initial=False,
                                           widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    user_company=forms.CharField(max_length=100, required=False)
    user_profile=forms.ImageField(required=False)

    def __init__(self,*args,**kwargs):
        self.instance=kwargs.pop('instance',None)
        super(ProfileUpdateForm,self).__init__(*args,**kwargs)

        if self.instance:
            self.initial['user_bio'] = self.instance.user_bio
            self.initial['phone_number'] = self.instance.phone_number
            self.initial['wanna_be_a_blogger'] = self.instance.wanna_be_a_blogger
            self.initial['user_company'] = self.instance.user_company
            self.initial['user_profile'] = self.instance.user_profile