# 🤖 Intelligent Multi-Modal Chatbot System

## 🚀 Overview
This project is an intelligent multi-modal chatbot capable of handling different types of user queries such as general questions, mathematical calculations, and image generation.  
The system dynamically routes queries to appropriate modules using intent detection.

---

## 🎯 Features
- 💬 Natural language responses using LLM (Groq API)
- ➗ Automatic detection and solving of math expressions
- 🎨 Image generation using Hugging Face model (FLUX.1-schnell)
- ⚡ Real-time response streaming using Server-Sent Events (SSE)
- 🔀 Intelligent query routing system

---

## 🧠 Architecture
User Query → Intent Detection →  
- Calculation → MCP Tool  
- General Query → Groq API  
- Image Request → Hugging Face API  
→ SSE Streaming → Response  

---

## 🛠️ Tech Stack
- Python  
- Groq API (LLM)  
- Hugging Face Inference API  
- MCP Server (for calculations)  
- SSE (Server-Sent Events)  
- Regex (for math detection)  

---

## ⚙️ Installation

```bash
git clone https://github.com/dh7-bit/chatbotmcpservergibliimages
cd chatbotmcpservergibliimages
pip install -r requirements.txt
