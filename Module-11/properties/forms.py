from django import forms
from .models import Property, RentalRequest, Review


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title',
            'description',
            'property_type',
            'location',
            'monthly_rent',
            'bedrooms',
            'bathrooms',
            'image',
            'availability_status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Modern 3-Bedroom Apartment in Gulshan-2'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe property amenities, floor level, utilities included, rules, etc.'
            }),
            'property_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Road 11, Banani, Dhaka'
            }),
            'monthly_rent': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monthly rent (BDT)',
                'min': '1',
                'step': '0.01'
            }),
            'bedrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '1'
            }),
            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '1'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'availability_status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_monthly_rent(self):
        rent = self.cleaned_data.get('monthly_rent')
        if rent is not None and rent <= 0:
            raise forms.ValidationError("Monthly rent must be greater than zero.")
        return rent

    def clean_bedrooms(self):
        beds = self.cleaned_data.get('bedrooms')
        if beds is not None and beds < 0:
            raise forms.ValidationError("Number of bedrooms cannot be negative.")
        return beds

    def clean_bathrooms(self):
        baths = self.cleaned_data.get('bathrooms')
        if baths is not None and baths < 0:
            raise forms.ValidationError("Number of bathrooms cannot be negative.")
        return baths


class RentalRequestForm(forms.ModelForm):
    class Meta:
        model = RentalRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Hello! I am interested in renting this property. Please let me know your availability for a visit or next steps.'
            })
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience staying in or renting this property...'
            })
        }


