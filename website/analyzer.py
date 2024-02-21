import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Define the symptoms_data
symptoms_data = [
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

# Convert the data to a flat list of symptoms and corresponding labels
flat_symptoms = [' '.join(entry['symptoms']) for entry in symptoms_data]
labels = [entry['Condition'] for entry in symptoms_data]

# Use LabelEncoder to convert Condition labels to numerical values
label_encoder = LabelEncoder()
labels_encoded = label_encoder.fit_transform(labels)

# Split the data into training and testing sets
flat_symptoms_train, flat_symptoms_test, labels_train, labels_test = train_test_split(flat_symptoms, labels, test_size=0.2, random_state=42)

# Combine training and test labels for label encoding
all_labels = labels_train + labels_test
label_encoder.fit(all_labels)

# Simple Dataset class
class SymptomsDataset(Dataset):
    def __init__(self, X, y, label_encoder):
        self.X = X
        self.y = y
        self.label_encoder = label_encoder

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        symptoms = self.X[idx].split()  # Split symptom string into individual symptoms
        symptom_vector = torch.tensor(self.label_encoder.transform(symptoms), dtype=torch.long)
        label = torch.tensor(self.label_encoder.transform([self.y[idx]]), dtype=torch.float32)
        return symptom_vector, label

# DataLoader for batch processing
train_dataset = SymptomsDataset(flat_symptoms_train, labels_train, label_encoder)
test_dataset = SymptomsDataset(flat_symptoms_test, labels_test, label_encoder)

# Define a simple neural network
class SymptomClassifier(nn.Module):
    def __init__(self):
        super(SymptomClassifier, self).__init__()
        self.embedding = nn.EmbeddingBag(num_embeddings=1000, embedding_dim=32, sparse=True)
        self.fc1 = nn.Linear(32, 16)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x):
        x = self.embedding(x)
        x = torch.flatten(x, start_dim=1)
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

# Initialize the model, loss function, and optimizer
model = SymptomClassifier()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(10):
    for inputs, labels in DataLoader(train_dataset, batch_size=32, shuffle=True):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels.float().view(-1, 1))
        loss.backward()
        optimizer.step()

# Evaluate on the test set
model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for inputs, labels in DataLoader(test_dataset, batch_size=32, shuffle=False):
        outputs = model(inputs)
        predicted = (outputs > 0.5).float()
        total += labels.size(0)
        correct += (predicted == labels.float().view(-1, 1)).sum().item()

accuracy = correct / total
print(f'Test Accuracy: {accuracy * 100:.2f}%')

# Save the trained model
torch.save(model.state_dict(), 'symptom_analyzer_model.pth')
