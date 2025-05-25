from django import forms
from django.core.exceptions import ValidationError
from .models import Product

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа',
                   'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_active':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            if field_name == 'image':
                field.widget.attrs['accept'] = 'image/jpeg, image/png'

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f'Название содержит запрещенное слово: "{word}"')
        return self.cleaned_data['name']

    def clean_description(self):
        description = self.cleaned_data['description'].lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(f'Описание содержит запрещенное слово: "{word}"')
        return self.cleaned_data['description']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Изображение не должно превышать 5 МБ')
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError('Допустимы только JPEG и PNG изображения')
        return image