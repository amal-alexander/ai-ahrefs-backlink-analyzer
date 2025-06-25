# Ahrefs Backlink Analysis App with Advanced Features
import streamlit as st
import pandas as pd
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import re
from openai import OpenAI
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

# --- Load environment variables ---
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# --- Upload & Preprocessing ---
def process_excel(file):
    try:
        df = pd.read_excel(file, engine='openpyxl')
        df['Domain'] = df['Referring page URL'].apply(lambda x: urlparse(str(x)).netloc if pd.notnull(x) else '')
        df_summary = df.groupby('Domain').agg({'Domain rating': 'max', 'Referring domains': 'max'}).reset_index()
        return df, df_summary
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None, None

# --- AI Query Fallback ---
def query_with_llm(prompt, df):
    try:
        minimal_df = df[['Referring page URL', 'Anchor', 'Domain rating', 'Nofollow']].copy()
        csv_data = minimal_df.head(50).to_csv(index=False)
        user_prompt = f"Data:\n{csv_data}\n\nQuestion: {prompt}"

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert SEO data analyst."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# --- Visualizations ---
def plot_rating_hist(df):
    fig = px.histogram(df, x='Domain rating', nbins=30, title="Domain Rating Distribution")
    st.plotly_chart(fig)

def anchor_wordcloud(df):
    text = ' '.join(str(a) for a in df['Anchor'] if pd.notnull(a))
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# --- Structured Queries ---
def process_query(prompt, df, df_summary):
    try:
        prompt_clean = re.sub(r'[^\w\s\d]', '', prompt.lower().strip())
        result_df, response_msg = None, ""

        if 'top' in prompt_clean and 'domains' in prompt_clean:
            match = re.search(r'top\s+(\d+)', prompt_clean)
            if match:
                n = int(match.group(1))
                result_df = df_summary.sort_values('Domain rating', ascending=False).head(n)
                response_msg = f"Top {n} domains by rating:"

        elif 'nofollow' in prompt_clean and 'high traffic' in prompt_clean:
            threshold = df['Page traffic'].quantile(0.75)
            result_df = df[(df['Nofollow']) & (df['Page traffic'] > threshold)]
            response_msg = "Nofollow backlinks from high traffic pages:"

        elif '404' in prompt_clean:
            result_df = df[df['Referring page HTTP code'] == 404]
            response_msg = "Broken backlinks (404):"

        elif 'anchor text' in prompt_clean:
            match = re.search(r'anchor text\s+([\w\s]+)', prompt_clean)
            if match:
                anchor = match.group(1).strip()
                result_df = df[df['Anchor'].str.contains(anchor, case=False, na=False)]
                response_msg = f"Backlinks using anchor text '{anchor}':"

        elif 'spammy' in prompt_clean or 'suspicious' in prompt_clean:
            result_df = df[(df['Domain rating'] < 10) & (df['Nofollow'])]
            response_msg = "Potentially spammy backlinks (low DR & nofollow):"

        else:
            llm_response = query_with_llm(prompt, df)
            return llm_response, None

        return response_msg, result_df
    except Exception as e:
        return f"Error: {str(e)}", None

# --- Streamlit UI ---
st.set_page_config("🔗 Advanced Backlink Analyzer", layout="wide")
st.title("🔗 Ahrefs Backlink Analysis Chatbot (Advanced)")

uploaded_file = st.file_uploader("📂 Upload Ahrefs Excel file", type=["xlsx", "xls"])

if 'df' not in st.session_state:
    st.session_state.df, st.session_state.df_summary = None, None

if uploaded_file:
    df, df_summary = process_excel(uploaded_file)
    if df is not None:
        st.session_state.df, st.session_state.df_summary = df, df_summary
        st.success("✅ File uploaded and processed.")

if st.session_state.df is not None:
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📊 Visuals", "📁 Filters", "⬇️ Export"])

    with tab1:
        st.markdown("### Ask any question about your backlinks")
        user_q = st.text_input("Ask here:")
        if user_q:
            reply, table = process_query(user_q, st.session_state.df, st.session_state.df_summary)
            st.markdown(f"**Bot:** {reply}")
            if table is not None:
                st.dataframe(table)

    with tab2:
        st.subheader("📉 Domain Rating Histogram")
        plot_rating_hist(st.session_state.df_summary)
        st.subheader("☁️ Anchor Text Word Cloud")
        anchor_wordcloud(st.session_state.df)

    with tab3:
        st.subheader("🔍 Filter Data")
        min_dr = st.slider("Minimum Domain Rating", 0, 100, 30)
        filtered = st.session_state.df[st.session_state.df['Domain rating'] >= min_dr]
        if st.checkbox("Show only dofollow"):
            filtered = filtered[~filtered['Nofollow']]
        st.dataframe(filtered)

    with tab4:
        st.subheader("⬇️ Export Filtered Data")
        buffer = io.BytesIO()
        filtered.to_excel(buffer, index=False, engine='openpyxl')
        st.download_button("Download as Excel", buffer.getvalue(), file_name="filtered_backlinks.xlsx")

else:
    st.info("Upload a file to begin analysis.")
