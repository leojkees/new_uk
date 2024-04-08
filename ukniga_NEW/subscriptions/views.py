from django.shortcuts import render
from .forms import CorporateSubscriptionForm, UserSubscriptionForm
from .models import Month
from subscriptions.models import Month
from datetime import datetime
from django.contrib import messages


# Функция для расчета стоимости подписки с учётом, что НДС уже включён
def calculate_total_cost(subscription_type, number_of_issues, amount):
    cost_per_issue = 1300 if subscription_type == 'paper' else 720
    total_cost = cost_per_issue * min(number_of_issues, 10) * amount
    return total_cost


def number_to_words_rub(n):
    if n > 13000:
        return "Сумма вне допустимого диапазона"
    
    units = ["", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
    tens = ["", "десять", "двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят", "семьдесят", "восемьдесят", "девяносто"]
    teens = ["десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"]
    hundreds = ["", "сто", "двести", "триста", "четыреста", "пятьсот", "шестьсот", "семьсот", "восемьсот", "девятьсот"]
    thousands = ["", "одна тысяча", "две тысячи", "три тысячи", "четыре тысячи", "пять тысяч", "шесть тысяч", "семь тысяч", "восемь тысяч", "девять тысяч", "десять тысяч", "одиннадцать тысяч", "двенадцать тысяч", "тринадцать тысяч"]
    
    if n == 0:
        return "ноль рублей"
    
    words = []
    if n >= 1000:
        words.append(thousands[n // 1000])
        n %= 1000
    
    if n >= 100:
        words.append(hundreds[n // 100])
        n %= 100
    
    if 10 < n < 20:
        words.append(teens[n - 10])
    else:
        if n >= 20:
            words.append(tens[n // 10])
        n %= 10
        if n > 0:
            words.append(units[n])
    
    if 10 < (n % 100) < 20:
        ruble_word = "рублей"
    else:
        ruble_word = ["рублей", "рубль", "рубля", "рубля", "рубля", "рублей", "рублей", "рублей", "рублей", "рублей"][n % 10]
    
    words.append(ruble_word)
    
    return " ".join(words)


# Представление для отображения и обработки формы подписки
def subscription_company(request):
    if request.method == 'POST':
        form = CorporateSubscriptionForm(request.POST)
        if form.is_valid():
            # Сохраняем форму, чтобы получить экземпляр модели с ID
            subscription = form.save()

            subscription_type = form.cleaned_data['type']

            # Стоимость за единицу в зависимости от типа подписки
            cost_per_issue = 1300 if subscription_type == 'paper' else 720

            # Здесь добавляем форматирование выбранных месяцев
            selected_issues = form.cleaned_data['issues']
            selected_month_names = [issue.name for issue in selected_issues.all()]
            # Преобразование списка названий месяцев в строку
            selected_months_str = ", ".join(selected_month_names)

            # Получаем данные из очищенных данных формы
            org_name = form.cleaned_data['org_name']
            corporate_address = form.cleaned_data['corporate_address']
            phone = form.cleaned_data['phone']
            inn = form.cleaned_data['inn']
            kpp = form.cleaned_data['kpp']
            subscription_type = form.cleaned_data['type']
            year = form.cleaned_data['year']
            issues = form.cleaned_data['issues']
            amount = form.cleaned_data['amount']

            # Предположим, функция calculate_total_cost возвращает только total_cost
            total_cost = calculate_total_cost(subscription_type, len(issues), amount)

            # Преобразование общей стоимости в словесное представление
            total_in_words = number_to_words_rub(total_cost)

            # Возможно, вам нужно добавить логику для определения type_caption, total_with_nds и total_in_words
            type_caption = 'Бумажный вариант' if subscription_type == 'paper' else 'Электронный вариант'
            total_with_nds = total_cost

            # Форматирование текущей даты и времени для отображения
            now = datetime.now()
            formatted_date = now.strftime("%d.%m.%Y")

            context = {
                'org_name': org_name,
                'corporate_address': corporate_address,
                'phone': phone,
                'inn': inn,
                'kpp': kpp,
                'invoice_id': subscription.id,  # ID сохраненной подписки как ID счета
                'date': formatted_date,
                'type_caption': type_caption,
                'year': year,
                'amount': amount,
                'cost_per_issue': cost_per_issue,
                'total_cost': total_cost,
                'total_with_nds': total_with_nds,
                'selected_months': selected_months_str,
                'total_in_words': total_in_words,  # Общая стоимость словами
            }

            return render(request, 'subscriptions/invoice.html', context)
        else:
            months = Month.objects.all()
            # Если форма недействительна, передайте ее обратно с сообщениями об ошибках
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Ошибка в поле '{form.fields[field].label}': {error}")
            return render(request, 'subscriptions/subscription_form.html', {'form': form, 'months': months})

    else:
        form = CorporateSubscriptionForm()
        months = Month.objects.all()
        return render(request, 'subscriptions/subscription_form.html', {'form': form, 'months': months})
    


def subscription_user(request):
    if request.method == 'POST':
        form = UserSubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save()

            subscription_type = form.cleaned_data['type']

            # Стоимость за единицу в зависимости от типа подписки
            cost_per_issue = 1300 if subscription_type == 'paper' else 720

            selected_issues = form.cleaned_data['issues']
            selected_month_names = [issue.name for issue in selected_issues.all()]
            selected_months_str = ", ".join(selected_month_names)

            contact = form.cleaned_data['contact']
            real_address = form.cleaned_data['real_address']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            year = form.cleaned_data['year']
            amount = form.cleaned_data['amount']

            total_cost = calculate_total_cost(subscription_type, len(selected_issues), amount)
            total_in_words = number_to_words_rub(total_cost)

            now = datetime.now()
            formatted_date = now.strftime("%d.%m.%Y")

            context = {
                'contact': contact,
                'real_address': real_address,
                'phone': phone,
                'email': email,
                'invoice_id': subscription.id,
                'date': formatted_date,
                'type_caption': 'Бумажный вариант' if subscription_type == 'paper' else 'Электронный вариант',
                'year': year,
                'amount': amount,
                'cost_per_issue': cost_per_issue,
                'total_cost': total_cost,
                'total_with_nds': total_cost,  # Если нет НДС, то это значение может быть таким же, как total_cost
                'selected_months': selected_months_str,
                'total_in_words': total_in_words,
            }

            return render(request, 'subscriptions/invoice_user.html', context)
        else:
            months = Month.objects.all()
            # Если форма недействительна, передайте ее обратно с сообщениями об ошибках
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Ошибка в поле '{form.fields[field].label}': {error}")
                return render(request, 'subscriptions/subscription_form_user.html', {'form': form, 'months': months})

    else:
        form = UserSubscriptionForm()
        months = Month.objects.all()
        return render(request, 'subscriptions/subscription_form_user.html', {'form': form, 'months': months})