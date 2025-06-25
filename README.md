# 🔗 AI Ahrefs Backlink Analyzer

AI-powered Streamlit app to analyze and explore backlinks from your Ahrefs export.  
Ask questions, find broken/spammy links, and visualize anchor usage — with optional GPT-4o support via OpenRouter.  

---

## 🚀 Features

- ✅ Upload `.xlsx` backlink file from Ahrefs
- 💬 Ask structured or open-ended questions
- 🔍 Detect spammy or broken backlinks
- ☁️ Anchor text word cloud visualization
- 📊 Domain Rating distribution chart
- 📁 Filter & export refined backlink data
- 🤖 GPT-4o fallback (OpenRouter) for complex SEO queries

---

## 📦 How to Use (Step-by-Step)

### 1️⃣ Download ZIP

- Click the green **`Code`** button at the top-right of this repo
- Select **`Download ZIP`**
- Unzip the folder anywhere on your system

### 2️⃣ Set up your Python environment

Open a terminal/command prompt in the extracted folder and run:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install streamlit pandas openpyxl python-dotenv openai plotly wordcloud matplotlib
```

### 3️⃣ Add your OpenRouter API Key

Create a `.env` file in the root folder:

```env
OPENROUTER_API_KEY=your_openrouter_key_here
```

> 💡 You can get a free GPT-4o key at https://openrouter.ai — no credit card required.  
> This enables AI fallback for open-ended SEO queries.

### 4️⃣ Launch the app

```bash
streamlit run app.py
```

You’ll see a local URL like `http://localhost:8501` — open it in your browser.

---

## 💡 Sample Questions to Ask

- Top 10 domains by rating  
- Show nofollow links with high traffic  
- Which links are broken?  
- What are the spammy backlinks?  
- Pages using “click here” as anchor  

---

## 🛠️ Built With

- [Streamlit](https://streamlit.io/)
- [OpenRouter (GPT-4o)](https://openrouter.ai/)
- [Pandas](https://pandas.pydata.org/)
- [WordCloud](https://github.com/amueller/word_cloud)
- [Plotly](https://plotly.com/python/)

> Connect with me 👉 [Amal Alexander](https://www.linkedin.com/in/amal-alexander-305780131/)  
