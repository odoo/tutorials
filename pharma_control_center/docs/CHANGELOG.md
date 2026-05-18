# Changelog

## 1.1 (May 18, 2026)

### ✨ New Features
- **🤖 AI Pharmacy Assistant Chatbot** – Intelligent conversational AI powered by Hugging Face Llama 3.1-8B
  - Context-aware responses using live pharmacy data (stock, orders)
  - Multi-turn conversation with chat history
  - Accessible to all authenticated users
  - Helpful for medicine information, dosage, and operations queries

- **🤖 Customer Sentiment Analysis** – AI-powered feedback classification
  - Analyzes customer feedback into Positive/Neutral/Negative
  - Manager-only access for quality monitoring
  - Quick one-step analysis via wizard interface
  - Supports service improvement initiatives

- **🔒 Privacy Policy & 📜 Terms of Service** – Comprehensive legal compliance
  - Built-in privacy policy with data protection terms
  - Full terms of service with medical disclaimer
  - Accessible to all users from main menu
  - Last updated tracking for transparency

### 🔧 Technical Improvements
- Added `pharmacy.ai.service` abstract model for Hugging Face API integration
- Added `pharmacy.chatbot` transient model for conversational interface
- Added `sentiment.analysis.wizard` transient model for feedback analysis
- Added `privacy.terms` transient model for legal documentation
- New views: `ai_views.xml` and `privacy_terms_views.xml`
- System parameter support for `HF_API_TOKEN` configuration

### 📋 Documentation Updates
- Updated README.md with AI features and privacy compliance sections
- Updated ARCHITECTURE.md with new models and menu items
- Updated TECHNICAL_DETAILS.md with AI service documentation
- Updated SECURITY.md with API configuration and access control
- Updated USER_GUIDE.md with chatbot and sentiment analysis tutorials

## 1.0 (April 29, 2026)

- Medicine catalog with expiry/reorder indicators
- Per-user cart with barcode quick add
- Checkout flow: Sales Order creation + invoice posting + custom stock reduction
- Dashboard KPIs and “today’s orders” drill-down
- Patient records with doctor assignment
- Drug interaction warnings + severe-interaction checkout blocking
- Manager sales analytics (graph/pivot on Sales Orders)

