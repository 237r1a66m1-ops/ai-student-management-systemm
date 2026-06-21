import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

# 1. Generate Synthetic Data
np.random.seed(42)
num_students = 200

attendance = np.random.randint(50, 100, size=num_students)
marks = np.random.randint(40, 100, size=num_students)
assignments = np.random.randint(40, 100, size=num_students)

# Rules for labeling: High Performer (2), Average Performer (1), At Risk (0)
performance_category = []
for i in range(num_students):
    score = (attendance[i] * 0.3) + (marks[i] * 0.5) + (assignments[i] * 0.2)
    if score >= 80:
        performance_category.append(2)  # High Performer
    elif score >= 60:
        performance_category.append(1)  # Average Performer
    else:
        performance_category.append(0)  # At Risk

df = pd.DataFrame({
    'attendance': attendance,
    'marks': marks,
    'assignments': assignments,
    'category': performance_category
})

# Save dataset
os.makedirs('ML', exist_ok=True)
df.to_csv('student_data.csv', index=False)
print("Dataset created successfully.")

# 2. Train Decision Tree
X = df[['attendance', 'marks', 'assignments']]
y = df['category']

# FIXED PARAMETER HERE (test_size=0.2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Test accuracy
accuracy = model.score(X_test, y_test)
print(f"Model trained with accuracy: {accuracy * 100:.2f}%")

# 3. Save Model safely to Backend folder
os.makedirs('../Backend', exist_ok=True)
with open('../Backend/student_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Model saved to Backend/student_model.pkl")