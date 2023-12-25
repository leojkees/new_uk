from django.shortcuts import render, get_object_or_404
from .models import Slider

def slider_view(request, slider_id):
    # Получите объект Slider по его уникальному ID
    slider = Slider.objects.get(slider_id=slider_id)
    
    # Передайте slider_id в контекст шаблона
    context = {
        'slider': slider,
        'slider_id': slider_id,  # Добавьте slider_id в контекст
    }

    return render(request, 'myapp/slider_template.html', context)



