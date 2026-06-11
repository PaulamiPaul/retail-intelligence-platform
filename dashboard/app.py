import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from groq import Groq
import warnings
warnings.filterwarnings('ignore')
import os
from dotenv import load_dotenv
load_dotenv('/Users/paulamipaul/Desktop/retail-intelligence-platform/.env')

st.set_page_config(page_title="Retail Intelligence Platform", layout="wide", page_icon="🛒")

engine = create_engine('postgresql://paulamipaul@localhost:5432/paulamipaul')

@st.cache_data
def load_data():
    with engine.connect() as conn:
        master = pd.read_sql(text("SELECT * FROM master_orders"), conn)
    return master

df = load_data()

st.title("🛒 Retail Intelligence Platform")
st.caption("Olist Brazilian E-Commerce — AI-Powered Analytics Dashboard")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Orders", f"{df['order_id'].nunique():,}")
with col2:
    revenue = df['payment_value'].sum()
    st.metric("Total Revenue", f"R${revenue:,.0f}")
with col3:
    avg_review = df['review_score'].mean()
    st.metric("Avg Review Score", f"{avg_review:.2f} / 5")
with col4:
    late = (df['delivery_delay_days'] > 0).sum()
    late_pct = late / len(df) * 100
    st.metric("Late Deliveries", f"{late_pct:.1f}%")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Categories by Revenue")
    cat_rev = (df.groupby('product_category_name_english')['payment_value']
               .sum().sort_values(ascending=False).head(10).reset_index())
    cat_rev.columns = ['Category', 'Revenue']
    fig1 = px.bar(cat_rev, x='Revenue', y='Category', orientation='h',
                  color='Revenue', color_continuous_scale='Blues')
    fig1.update_layout(showlegend=False, coloraxis_showscale=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Monthly Order Volume")
    df['month'] = pd.to_datetime(df['order_purchase_timestamp']).dt.to_period('M').astype(str)
    monthly = df.groupby('month').size().reset_index(name='orders')
    fig2 = px.line(monthly, x='month', y='orders', markers=True)
    fig2.update_layout(height=400, xaxis_tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("Average Review Score by Category (Top 15)")
review_cat = (df.groupby('product_category_name_english')['review_score']
              .mean().sort_values(ascending=False).head(15).reset_index())
review_cat.columns = ['Category', 'Avg Score']
fig3 = px.bar(review_cat, x='Category', y='Avg Score',
              color='Avg Score', color_continuous_scale='RdYlGn',
              range_color=[3.5, 5])
fig3.update_layout(height=400, xaxis_tickangle=45, coloraxis_showscale=False)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.subheader("🤖 Ask the AI Agent")
st.caption("Ask any business question about the retail data in plain English")

question = st.text_input("Your question:", placeholder="e.g. Which sellers have the most 5-star reviews?")

if question:
    client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=[
                {
                    'role': 'user',
                    'content': (
                        "You are a PostgreSQL expert. You have ONE table called master_orders with these columns:\n"
                        "order_id, customer_id, order_status, order_purchase_timestamp,\n"
                        "order_delivered_customer_date, delivery_delay_days, processing_time_days,\n"
                        "product_id, seller_id, price, freight_value,\n"
                        "product_category_name_english, customer_city, customer_state,\n"
                        "seller_city, seller_state, review_score, review_comment_message, payment_value\n\n"
                        "RULES:\n"
                        "- Use ONLY the master_orders table. No JOINs. No subqueries referencing other tables.\n"
                        "- Return ONLY the SQL query, nothing else.\n"
                        "- Use LIMIT 15.\n\n"
                        f"Question: \"{question}\"\n"
                        "SQL:"
                    )
                }
            ]
        )
        sql = response.choices[0].message.content.strip().replace('```sql','').replace('```','').strip()

    st.code(sql, language='sql')

    try:
        with engine.connect() as conn:
            result = pd.read_sql(text(sql), conn)
        st.dataframe(result, use_container_width=True)
    except Exception as e:
        st.error(f"SQL Error: {e}")