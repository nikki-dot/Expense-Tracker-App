# Personal Expense Tracker

## 📌 Project Overview
The **Personal Expense Tracker** is a web application that helps users keep track of their daily spending and gain insights into their financial habits.

I chose this project because expense tracking is a real-life challenge faced by many people. The app provides a user-friendly way to log expenses, view spending summaries, and analyze patterns over time.

Built with **Python** and **Streamlit**, the app uses **Pandas** for data handling and **Altair** + **Plotly** for interactive data visualization. Streamlit made it easy to build a **clean, interactive, and visually appealing UI** without traditional web development complexity. 

### ✨ Features:
- User-friendly sidebar to input expenses
- **AI-powered insights** to monitor budgets and top spending areas
- **Visual Analytics**: Bar and Pie charts to show category-wise spending
- Weekly and monthly spending summaries
- Sorted expense table with formatted currency display
- A welcoming card for new users with no expenses added yet

---

## 🛠️ Technologies Used
- **Language:** Python
- **Framework:** Streamlit
- **Libraries:** Pandas, Altair, Plotly
- **Project Type:** Web Application with Data Visualization

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/nikki-dot/Expense-Tracker-App.git
cd Expense-Tracker-App
```

### 2. Install dependencies
Create a `requirements.txt` file:
```
streamlit==1.42.0
pandas==2.2.3
altair==5.0.1
plotly==5.24.1
```

Install them:
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run tracker.py
```

---

## 🚀 Development Journey
1. Set up the basic Streamlit structure with headings and input fields.
2. Added a **sidebar** to capture Category, Amount, Date, and Description from users.
3. Stored all expenses in a **Pandas DataFrame** using `st.session_state`.
4. Calculated key metrics: Total amount spent, Number of expenses, Weekly & Monthly totals.
5. Added **AI-powered insights** to give budget warnings and highlight top-spending categories.
6. Designed **Visual Analytics** using Altair bar charts and Plotly pie charts.
7. Added a **welcome card** for new users (shown only when no expenses exist).
8. Enhanced the UI with **CSS styling** for cards, graphs, and layouts.

---

## 🔑 Features Implemented
- Interactive sidebar for expense entry
- Weekly and monthly summaries
- AI-generated spending insights
- Visualization by category (Bar & Pie charts)
- Table view of expenses sorted by date
- Simple and intuitive UI

---

## 🛠️ Challenges & Solutions
- **Altair chart labels:** Needed values on top of bars → Googled and used Altair `mark_text`.
- **KeyError `'Amount'`:** After `groupby()`, converted Series back to DataFrame with `.reset_index()`.
- **Welcome card visible after adding expenses:** Fixed Python **indentation issue**.
- **Graph styling:** Used ChatGPT suggestions to customize graphs.
- **Currency formatting:** Used **Lambda function** for ₹ formatting in the table.
- **AI insights not showing:** Fixed **indentation** and function call errors.

---

## 📈 Learning Outcomes
- Building interactive web apps using **Streamlit**
- Data manipulation and summarization with **Pandas**
- Styling and creating **Altair & Plotly** charts
- Debugging common Python errors
- Maintaining state in Streamlit with `st.session_state`
- Writing cleaner, maintainable, and user-friendly code

---

## 🏆 Conclusion
This project was a valuable learning experience combining **problem-solving, data visualization, UI design, and debugging**.  
It not only helped me understand my own expenses but also showcased how to build a **real-world financial tracking tool** using Python and Streamlit.

---

## 📂 Repository Structure
```
Expense-Tracker-App/
│
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── screenshots/          # App UI screenshots
```

---

## 🔗 Future Improvements
- Add authentication for multiple users
- Export expense data as CSV/PDF
- Deploy on **Render**, **HuggingFace Spaces**, or **Streamlit Cloud**
- Introduce predictive analysis for future budgeting
