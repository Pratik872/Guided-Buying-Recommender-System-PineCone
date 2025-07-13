import streamlit as st
import json
import time
from src.gbr_system import GBRSystem
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from config.constants import *

# Load environment variables
load_dotenv()
pc_key = os.getenv('PINECONE_API_KEY')

@st.cache_resource
def load_model():
    return SentenceTransformer('all-mpnet-base-v2')

# Initialize session state
if 'gbr_system' not in st.session_state:
    # Initialize components
    pc = Pinecone(api_key=pc_key)
    idx = pc.Index(index_name)

    retriever = load_model()
    
    ner_engine = pipeline("ner", 
                         model="Babelscape/wikineural-multilingual-ner",
                         aggregation_strategy="simple")
    
    st.session_state.gbr_system = GBRSystem(idx, retriever, ner_engine)

# Load user profiles
@st.cache_data
def load_user_profiles():
    with open('config/user_profiles.json', 'r') as f:
        return json.load(f)

# App header
st.set_page_config(page_title="GBR System", page_icon="🛒", layout="wide")
st.title("🛒 Guided Buying Recommender System")
st.markdown("*AI-powered procurement platform for enterprise purchasing decisions*")
st.divider()

# Sidebar - User Profile Selection
st.sidebar.header("👤 User Profile")
profiles = load_user_profiles()
profile_names = list(profiles.keys())
selected_profile = st.sidebar.selectbox("Select Role:", profile_names)

# Display selected profile with better formatting
with st.sidebar.expander("📋 Profile Details", expanded=True):
    profile = profiles[selected_profile]
    st.metric("Budget", f"${profile['budget']:,}")
    st.write(f"**Categories:** {', '.join(profile['categories'])}")

# Main search interface with better layout
col1, col2 = st.columns([3, 1])
with col1:
    st.header("🔍 Product Search")
    query = st.text_input("", placeholder="e.g., I need a Dell laptop for development work", label_visibility="collapsed")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("🔍 Search Products", type="primary", use_container_width=True)
    
# Search execution
if search_button and query:
    with st.spinner("Searching products and generating recommendations..."):
        start_time = time.time()
        
        # Execute complete GBR workflow
        results = st.session_state.gbr_system.process_query(
            query=query, 
            user_profile=profiles[selected_profile]
        )
        
        search_time = (time.time() - start_time)
    
    # Display search results
    search_results = results['search_results']
    if search_results:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.success(f"✅ Found {len(search_results)} products")
        with col2:
            st.info(f"⚡ Search time: {search_time:.1f}s")
        
        st.header("📦 Search Results")
        
        for i, product in enumerate(search_results):
            # Product card with border
            with st.container(border=True):
                # Header row
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.subheader(f"{i+1}. {product['title'][:60]}...")
                    st.caption(f"ID: {product['id']}")
                
                with col2:
                    if product['price'] > 0:
                        st.metric("💰 Price", f"${product['price']:,.2f}")
                    else:
                        st.metric("💰 Price", "N/A")
                
                with col3:
                    if product['stars'] > 0:
                        st.metric("⭐ Rating", f"{product['stars']:.1f}")
                    else:
                        st.metric("⭐ Rating", "N/A")
                
                with col4:
                    st.metric("📝 Reviews", f"{product['reviews']:,}")
                
                # Details row
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Full Title:** {product['title']}")
                    st.link_button("🔗 View on Amazon", product['productURL'], use_container_width=True)
                
                with col2:
                    budget = profiles[selected_profile]['budget']
                    if product['price'] > 0:
                        if product['price'] <= budget:
                            st.success("✅ Within Budget")
                            savings = budget - product['price']
                            st.caption(f"💰 Saves ${savings:,.2f}")
                        else:
                            over_budget = product['price'] - budget
                            st.error(f"❌ Over Budget")
                            st.caption(f"💸 Exceeds by ${over_budget:,.2f}")
                    else:
                        st.info("💰 Price TBD")
        
        # Display bundle recommendations
        bundles = results['bundles']
        if bundles:
            st.header("📦 Bundle Recommendations")
            st.markdown("*Complete your purchase with these complementary products*")
            
            for i, bundle in enumerate(bundles):
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.subheader(f"Bundle {i+1}: {bundle['main_product']['title'][:50]}...")
                        
                        # Show accessories
                        st.markdown("**Included accessories:**")
                        for acc in bundle['accessories']:
                            st.markdown(f"• {acc['title'][:60]}... - ${acc['price']:.2f}")
                    
                    with col2:
                        st.metric("💰 Bundle Price", f"${bundle['total_price']:,.2f}")
                        st.metric("💸 You Save", f"${bundle['savings']:.2f}")
                        
                        if bundle['total_price'] <= profiles[selected_profile]['budget']:
                            st.success("✅ Within Budget")
                        else:
                            st.error("❌ Over Budget")
        
        # Display alternatives
        alternatives = results['alternatives']
        if alternatives:
            st.header("🔄 Alternative Options")
            st.markdown("*Similar products you might consider*")
            
            col1, col2, col3 = st.columns(3)
            for i, alt in enumerate(alternatives):
                with [col1, col2, col3][i % 3]:
                    with st.container(border=True):
                        st.markdown(f"**{alt['title'][:40]}...**")
                        st.metric("Price", f"${alt['price']:,.2f}")
                        st.metric("Match", f"{alt['score']:.2f}")
                        st.link_button("View", alt['productURL'], use_container_width=True)
    
    else:
        st.warning("⚠️ No products found. Try adjusting your search query or profile settings.")

# Footer
st.markdown("---")
st.markdown("*Built with Pinecone Vector DB, SentenceTransformers, and Streamlit*")