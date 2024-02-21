from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, SymptomAnalyzerForm
from .models import Record

# Define the predict_condition function based on your provided symptoms_data
def predict_condition(symptoms):
    # Replace this with your actual logic for predicting the condition based on symptoms
    conditions_data = [
        {'Condition': 'Malaria', 'symptoms': ['Fever', 'Chills', 'Headache', 'Muscle_ache', 'Fatigue', 'Nausea', 'Vomiting', 'Diarrhea']},
        {'Condition': 'Tuberculosis', 'symptoms': ['Cough', 'Weight_loss', 'Night_sweats', 'Fatigue', 'Chest_pain', 'Bloody_cough']},
        {'Condition': 'HIV/AIDS', 'symptoms': ['Fatigue', 'Weight_loss', 'Fever', 'Night_sweat', 'Recurrent_infection']},
        {'Condition': 'Gastroenteritis', 'symptoms': ['Diarrhea', 'Abdominal_pain', 'Cramps', 'Nausea', 'Vomiting']},
        {'Condition': 'Typhoid', 'symptoms': ['High_fever', 'Headache', 'Abdominal_pain', 'Constipation', 'Diarrhea', 'Weakness']},
        {'Condition': 'Cholera', 'symptoms': ['Water_diarrhea', 'Vomiting', 'Rapid_heart_rate', 'Dehydration', 'Muscle_cramps']},
        {'Condition': 'Diabetes', 'symptoms': ['Frequent_urination', 'Excessive_thirst', 'Weight_loss', 'Fatigue', 'Blurred_vision']},
        {'Condition': 'Hypertension', 'symptoms': ['High_blood_pressure', 'Headache', 'Dizziness', 'Chest_pain', 'Fatigue']},
        {'Condition': 'Pneumonia', 'symptoms': ['Phlegm_cough', 'Chest_pain', 'Loss_of_breath', 'Fever', 'Fatigue']},
        {'Condition': 'Dengue_Fever', 'symptoms': ['High_fever', 'Severe_headache', 'Pain_in_eyes', 'Joint_pain', 'Muscle_pain', 'Rash']}
    ]
    
    # Check if any symptom matches with predefined conditions
    for condition_data in conditions_data:
        if set(symptoms) == set(condition_data['symptoms']):
            return condition_data['Condition']

    # Default condition if no match is found
    return 'Unknown Condition'

def home(request):
    records = Record.objects.all()

    # Check if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
        else:
            messages.error(request, "Login error")

    symptom_form = SymptomAnalyzerForm()  # Create an instance of SymptomAnalyzerForm
    return render(request, 'home.html', {'records': records, 'symptom_form': symptom_form})


def logout_user(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "Registration successful")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

def symptom_analyzer(request):
    if request.method == 'POST':
        form = SymptomAnalyzerForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data['symptoms']
            
            # Now, you need to pass the symptoms to your prediction function
            condition = predict_condition(symptoms)
            
            messages.success(request, f"Symptom analysis successful. Predicted condition: {condition}")
            return redirect('home')
    
    return redirect('home')