# Example: Email Classification with Naive Bayes

The main goal of this algorithm is to demonstrate how the Naive Bayes method can be very effective in classification tasks, such as spam detection. Below, we present an easy-to-understand step-by-step guide so you can reproduce the implementation with other datasets and practice while having fun! 😄

<img src="https://media1.tenor.com/m/3AQDvhSiPpMAAAAC/dog-hacker.gif" width="300" />

## Code

### Import Libraries
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

- pandas as pd → to read the CSV and manipulate the DataFrame.
- MultinomialNB → Naive Bayes classifier.
- train_test_split → splitting between training and testing.
- TfidfVectorizer → transforms text into numbers.
- SMOTE → to balance the dataset.
- Counter → a data structure used to count the frequency of elements in an iterable.
- confusion_matrix, seaborn, matplotlib.pyplot → to visualize the confusion matrix.

### Load and Prepare the Data
ds = pd.read_csv("/content/spam.csv")
ds["spam"] = ds["Category"].apply(lambda x: 1 if x == "spam" else 0)
y = ds.iloc[:, 2].values
X = ds["Message"]
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42, stratify=y)

- Loads the CSV dataset → reads the file `spam.csv` and stores it in the DataFrame `ds` using pandas.
- Creates a new column "spam" with binary labels (0 and 1):
  - Accesses the `Category` column containing text labels like "spam" or "ham" (non-spam).
  - Uses `apply()` with a lambda function to convert these texts into numbers: "spam" → 1, any other value (like "ham") → 0.
  - Creates a new column `spam` in the DataFrame with these values.
- Separates the labels (`y`).
- Separates the messages (`X`).
- Vectorization with TfidfVectorizer → converts the texts in the `Message` column into sparse numerical vectors based on term frequency and importance (TF-IDF = Term Frequency – Inverse Document Frequency).
- Splits the data into 80% training and 20% testing → `stratify=y` ensures the class proportion (spam/ham) remains the same in both sets.
- `random_state = 42` → ensures reproducibility.
- `stratify = y` → guarantees class balance in both sets.

> [!IMPORTANT]  
> Without `stratify`, the model could end up with too few spam examples in the training or test set, which would harm learning and evaluation.

> [!Note]  
>Why use TF-IDF?  
> - Gives higher weight to words that really matter.  
> - Ignores common words (like "and", "the", "of", etc.).  
> - Fast and efficient.  
> - Works very well with linear models like Naive Bayes.

### Oversampling
Generate synthetic data for the minority class (in this case, spam).

> [!Note]  
>Oversampling is a technique in machine learning to handle imbalanced datasets — when one class (e.g., spam) has far fewer examples than the other (e.g., non-spam).

print("Before oversampling:", Counter(y_train))

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

- Creates a SMOTE object to generate synthetic examples for the minority class (spam = 1).  
- SMOTE performs oversampling:
  - It generates synthetic examples of the minority class.  
  - The resulting training set (`X_train_smote`) now has the same number of examples for both classes.

print("After oversampling:", Counter(y_train_smote))

### Train, Test, and Visualize Results
model = MultinomialNB()
model.fit(X_train_smote, y_train_smote)
predictions = model.predict(X_test)
predictions

y_test

model.score(X_test, y_test)

cm = confusion_matrix(y_test, predictions)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

- To visualize the model’s predictions, we use the confusion matrix, which shows in detail how many correct and incorrect predictions were made for each class (spam and non-spam).

### Conclusions
📌 ***The model is effective for detecting spam***  
  - Correctly classifies most messages, as shown by the high accuracy of 97%.  
  - It can correctly predict both spam and non-spam, confirmed by the confusion matrix.

📌 ***Using SMOTE was essential***  
  - With oversampling, the number of examples in each class is balanced, which helps the model learn better how to identify spam.  
  - Prevents the model from "ignoring" the minority class (spam).

📌 ***Well-structured pipeline***  
  - Preprocessing.  
  - Vectorization.  
  - Stratified splitting.  
  - Balance with SMOTE.  
  - Training.  
  - Evaluation with metrics and confusion matrix.

## 👾 **Contributors**  
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/112569754?v=4" width=115><br><sub>Alice Motin</sub>](https://github.com/AliceMotin) |  
| :---: | 