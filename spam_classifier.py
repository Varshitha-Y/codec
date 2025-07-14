import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ✅ Load CSV (assuming it's tab-separated and no header)
df = pd.read_csv('spam.csv', sep='\t', header=None, names=['label', 'message'])

# ✅ Convert labels: ham → 0, spam → 1
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# ✅ Split into train/test
X_train, X_test, y_train, y_test = train_test_split(df['message'], df['label'], test_size=0.2, random_state=42)

# ✅ Convert text to features
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ✅ Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# ✅ Evaluate the model
y_pred = model.predict(X_test_vec)

print("==== Spam Classifier Evaluation ====\n")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}\n")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ✅ Predict a sample message
def predict_message(msg):
    msg_vec = vectorizer.transform([msg])
    prediction = model.predict(msg_vec)[0]
    return "Spam" if prediction == 1 else "Not Spam"

test_msg = "Congratulations! You've won a free ticket. Reply now to claim."
print(f"\nTest message: \"{test_msg}\"")
print("Prediction:", predict_message(test_msg))