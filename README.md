# vro_project

## Project 1: VRO Buddy Avatar

## Project 2: Search- First VRO Buddy 


# VRO Buddy - VRO Buddy Avatar 

## 🤖 **Overview**

**TTS Engine:** [ElevenLabs](https://elevenlabs.io)  
**Lip-Sync Engine:** [D-ID API](https://www.d-id.com/)  
**Languages Supported:** English, Hindi  
**Instructions:**
1. Add `ELEVENLABS_API_KEY` and `DID_API_KEY` in `.streamlit/secrets.toml`
2. Upload the static image `vro_avatar.png`
3. Enter your intro script and click *Generate VRO Buddy Intro*.
4. The app will create a multilingual lip-synced avatar video.


# 🛍️ VRO Buddy – Search-First AI Shopping Companion

## 📖 Overview

VRO Buddy is a prototype **AI shopping assistant** that helps users discover products from a catalog using **search-based discovery only**.  
It uses **text embeddings + vector similarity** to return the most relevant matches for user queries like:

> “blue sneakers under ₹5,000”  
> “black leather jacket for winter”

This app was built as part of **Project 2: Search-First VRO Buddy**.

---

## 🎯 Objectives
- Enable **keyword-based product search** (no chat-style conversation)
- Support **multi-modal display**: product name, description, price, image
- Allow **filters** (category, price range)
- Implement **optional personalization** (liked items)
- Deliver a **clean Streamlit prototype** for demonstration

---

Demo : https://searchvro.streamlit.app/

## 🧠 Features

✅ **Search-Based Discovery**  
- Query using natural phrases or keywords  
- Filter by category and price range  

✅ **Multi-Modal Display**  
- Products shown with image, name, description, price, category  

✅ **Personalization (Optional)**  
- Track items “liked” by user in-session  
- Display user’s liked items below results  

✅ **Vector Search with Embeddings**  
- Uses `SentenceTransformers` for semantic similarity  

✅ **Lightweight UI**  
- Built with Streamlit for simplicity and easy cloud deployment  

---
