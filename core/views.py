from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.ai_models.siem import *
from core.ai_models.siem_comp import *
from core.ai_models.data_prep import process_logs 
from core.ai_models.isolation_f import *
from core.nlp.gptkey import *
from core.nlp.llama import *

def home_view(request):
    return render(request, 'homepage.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            error_message = 'Invalid username or password.'

    return render(request, 'login.html', {'error_message': error_message})

def signup_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            error_message = 'Username already exists. Please choose a different one.'
        elif User.objects.filter(email=email).exists():
            error_message = 'Email already exists. Please use a different one.'
        else:
            User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')  

    return render(request, 'register.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login') 


from django.shortcuts import render
from django.http import HttpResponse

def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')

        if file:
            # Assuming you have a media directory configured in your Django settings
            with open(f'media/{file.name}', 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            logs_df = process_logs(f'media/{file.name}', percentage=0.001)
            save_size_vs_status_scatter_plot(logs_df)
            save_status_distribution_bar_chart(logs_df)
            save_traffic_label_distribution_pie_chart(logs_df)
            save_requests_over_time_time_series_plot(logs_df)
            save_size_by_traffic_label_box_plot(logs_df)
            return redirect('dashboard')

    return render(request, 'upload.html')


def anomaly(request):
    logs_df = process_logs(f'media/access.log', percentage=0.001)
    features = ['encoded_refers', 'encoded_user-agent', 'encoded_status', 'encoded_method']

    isolation_scores, scaler, isolation_model = train_isolation_forest(logs_df, features)
    evaluate_anomaly_detection(isolation_scores, (isolation_scores < 0).astype(int))
    # Example usage
    plot_anomaly_detection_with_pie(isolation_scores)
    save_anomaly_logs(logs_df, isolation_scores, threshold=0)

    return render(request, 'anomaly.html')


def read_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def get_threat_solution(request):
    file_path = '/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/text_files/anomaly_logs.txt'

    if request.method == 'POST':
        selected_lines = int(request.POST.get('selected_lines', 50))

        # Read logs from the file
        with open(file_path, 'r') as file:
            logs = file.readlines()

        selected_logs = logs[1:selected_lines]
        
        threat = generate_prompt(f'you are a cyber security expert in my company and you have to find threats in these selected lines of logs, try to find what threats these logs can be able to create , the logs are this {selected_logs}')
        solution = generate_prompt(f'you are a cyber security expert in my company and you have to find solution of these selecteed logs ,the logs are this{selected_logs} , try to find best and legit solution for these logs')
        
        return render(request, 'nlp.html', {'threat': threat, 'solution': solution,'logs':selected_logs})

    return render(request, 'nlp.html')


def llama(request):
    file_path = '/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/text_files/anomaly_logs.txt'

    if request.method == 'POST':
        selected_lines = int(request.POST.get('selected_lines', 50))

        # Read logs from the file
        with open(file_path, 'r') as file:
            logs = file.readlines()

        selected_logs = logs[1:selected_lines]
        
        threat = run_chatbot(f'you are a cyber security expert in my company and you have to find threats in these selected lines of logs, try to find what threats these logs can be able to create , the logs are this {selected_logs}')
        solution = run_chatbot(f'you are a cyber security expert in my company and you have to find solution of these selecteed logs ,the logs are this{selected_logs} , try to find best and legit solution for these logs')
        
        return render(request, 'llama.html', {'threat': threat, 'solution': solution})

    return render(request, 'llama.html')


def other_models(request):
    return render(request, 'kmean.html')