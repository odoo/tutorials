# AI Features Guide

Pharma Control Center v1.1 includes intelligent AI-powered features using Hugging Face's Llama 3.1-8B language model for enhanced user experience and operational insights.

---

## 🤖 Overview

The module provides two AI-powered tools:

1. **AI Pharmacy Assistant Chatbot** – Conversational assistant for medicines and operations
2. **Sentiment Analysis Tool** – Analyzes customer feedback for quality insights

Both features are powered by the same LLM backend and require a Hugging Face API token.

---

## 🔧 Technical Architecture

### API Integration

**Service Model:** `pharmacy.ai.service` (AbstractModel)

- **Backend:** Hugging Face Inference API
- **Model:** `meta-llama/Llama-3.1-8B-Instruct:novita`
- **Endpoint:** `https://router.huggingface.co/v1/chat/completions`
- **Authentication:** Bearer token via `HF_API_TOKEN` system parameter

### Configuration Requirements

**System Parameter Setup:**
```
Key:   HF_API_TOKEN
Value: Your Hugging Face API Token
```

**Obtaining a Token:**
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Choose "Read" permissions (sufficient for inference)
4. Copy the token
5. Paste into Odoo System Parameters

---

## 💬 AI Pharmacy Assistant Chatbot

### Overview

The chatbot provides intelligent, context-aware responses about pharmacy operations, medicines, dosage information, and system usage.

**Model:** `pharmacy.chatbot` (TransientModel)  
**Access:** All authenticated users (`base.group_user`)  
**Menu:** **💊 Your Pharma CC → 🤖 AI Assistant**

### Features

#### Context-Aware Responses
- **Live Data Injection:** Automatically enriches responses with real-time pharmacy data
- **Medicine Stock Info:** When asked about a medicine, provides current availability
- **Today's Orders Summary:** Retrieves and includes today's order statistics when relevant
- **Smart Matching:** Uses both full and partial name matching for medicines

#### Conversation Features
- **Chat History:** Maintains conversation history within the session
- **Message Formatting:** User messages prefixed with 🧑‍⚕️, AI responses with 🤖
- **Error Handling:** Gracefully handles API errors and displays helpful messages
- **Session Persistence:** History is preserved while the wizard is open

#### Technical Parameters
- **Temperature:** 0.7 (balanced creativity and consistency)
- **Max Tokens:** 500 (approximately 2-3 paragraphs of response)
- **Timeout:** 30 seconds per API call

### Usage Examples

**Example 1: Medicine Stock Query**
```
User: "How many units of Aspirin do we have?"
→ AI automatically fetches medicine data
→ Response: "Medicine 'Aspirin 500mg' has 45 units in stock."
```

**Example 2: Today's Orders**
```
User: "What are today's orders?"
→ AI fetches orders from today
→ Response: "Today there are 12 orders, total amount: $5,432.50."
```

**Example 3: General Pharmacy Question**
```
User: "Tell me about Paracetamol"
→ AI provides information from system prompt
→ Response: "Paracetamol is an analgesic and antipyretic. 
   Common uses include pain relief and fever reduction. 
   Always consult a doctor for medical advice."
```

### System Prompt

The chatbot operates under a comprehensive system prompt:

```
You are a helpful assistant for the Pharma Control Center Odoo module. 
Features include medicine catalog, patient management, cart ordering, 
dashboard, role-based access, drug interaction warnings, reports, etc.

[Optional live data injected here]

Answer the user's question accurately using the live data if relevant. 
Always remind users to consult a doctor for medical advice. 
Keep answers concise and friendly.
```

### Implementation Details

**Key Methods:**
- `action_send_message()` – Processes user message and gets AI response
- `chat()` (in pharmacy.ai.service) – Orchestrates message sending to API
- `_get_medicine_stock_info()` – Extracts medicine name and returns inventory
- `_get_today_orders_info()` – Fetches today's order statistics

**Data Sources:**
- `pharmacy.medicine` model for stock information
- `sale.order` model for order statistics
- Date filtering for "today's orders"

### Error Handling

**Common Errors:**

1. **"HF_API_TOKEN not set in system parameters."**
   - Solution: Configure the token in Settings → Technical → Parameters

2. **"AI service error: Connection refused"**
   - Solution: Verify internet connection and Hugging Face API status
   - Check if HF_API_TOKEN is valid

3. **Token Timeout (>30 seconds)**
   - Solution: Retry the request; API may be temporarily slow
   - Check Hugging Face status page

---

## 🎯 Sentiment Analysis Tool

### Overview

Analyzes customer feedback to classify sentiment and support quality monitoring initiatives.

**Model:** `sentiment.analysis.wizard` (TransientModel)  
**Access:** Managers only (`pharma_control_center.group_pharmacy_manager`)  
**Menu:** **💊 Your Pharma CC → 🤖 AI Sentiment Analysis**

### Features

#### Sentiment Classification
- **Output:** One-word response (Positive, Neutral, or Negative)
- **Accuracy:** Trained on diverse feedback samples
- **Speed:** Typically <5 seconds per analysis
- **Batch Ready:** Can analyze multiple feedback items sequentially

#### Use Cases
- Customer satisfaction monitoring
- Quality improvement initiatives
- Feedback categorization
- Trend analysis over time
- Service improvement planning

### Usage Workflow

**Step 1: Access Tool**
- Click menu: **💊 Your Pharma CC → 🤖 AI Sentiment Analysis**
- Modal dialog opens with feedback input

**Step 2: Enter Feedback**
- Paste or type customer feedback in the text field
- Can be multi-line feedback

**Example feedbacks:**
```
"Great service! Fast delivery and excellent customer support!"
→ Positive

"The order arrived but the product was damaged in transit."
→ Negative

"Everything was okay, nothing special."
→ Neutral
```

**Step 3: Analyze**
- Click **Analyze Sentiment** button
- Wait for API response

**Step 4: View Result**
- Sentiment appears in the readonly result field
- Can analyze more feedback by clearing and repeating

### System Prompt for Sentiment Analysis

```
You are a customer sentiment analyst. 
Respond ONLY with one word: Positive, Neutral, or Negative.

Analyze the sentiment of this feedback: '[user_feedback]'
```

### Implementation Details

**Key Method:**
- `action_analyze()` – Calls AI service and returns result

**Data Flow:**
1. User enters feedback text
2. `action_analyze()` calls `pharmacy.ai.service.analyze_sentiment()`
3. AI service sends structured message to Hugging Face API
4. Response extracted (expecting single word)
5. Result displayed to user

### Best Practices

**Effective Feedback Analysis:**
- Input complete customer sentences (not fragments)
- Preserve original language (supports multiple languages via LLM)
- Batch similar feedback to identify trends
- Use results to prioritize improvements

**Tips for Better Insights:**
- Analyze feedback periodically (weekly/monthly) to track trends
- Combine with numerical ratings for richer insights
- Share results with operations team for action items
- Document improvements made based on feedback

---

## 🔐 Privacy & Compliance

### Data Privacy

**What Gets Sent to Hugging Face?**
- User messages (for chatbot)
- Customer feedback text (for sentiment analysis)
- Live pharmacy data (medicine names, quantities, order counts)

**What Does NOT Get Sent:**
- Patient medical records
- User credentials or passwords
- Internal system configurations

### API Security

- Communication uses HTTPS (encrypted in transit)
- API token is stored securely in Odoo database (read-only to users)
- Hugging Face API complies with data protection standards
- No data is stored on Hugging Face servers after response is sent

### Compliance Notes

- GDPR compliant (data is not retained on external servers)
- Suitable for healthcare environments
- API responses include safety guidelines (e.g., "consult a doctor")
- Manager-only access for sentiment analysis (administrative control)

---

## 🛠️ Customization & Extension

### Adding Custom Data Sources

To enrich chatbot responses with additional data:

```python
# In models/pharmacy_ai_service.py
def _get_custom_data(self, user_message):
    """Custom method to fetch additional context."""
    # Query your data
    data = self.env['your.model'].search(...)
    # Format and return
    return formatted_data

# Then modify chat() method to include new data
def chat(self, user_message, conversation_history=None):
    live_data = ""
    custom_data = self._get_custom_data(user_message)
    if custom_data:
        live_data += f"\n\nCustom Data:\n{custom_data}\n"
    # ... rest of implementation
```

### Changing the LLM Model

To use a different model:

```python
# In models/pharmacy_ai_service.py
def _call_llm(self, messages, model="your-new-model-name"):
    # Change default model name here
    # Must be compatible with Hugging Face Inference API
```

### Adjusting Response Parameters

```python
# In models/pharmacy_ai_service.py
payload = {
    "messages": messages,
    "model": model,
    "temperature": 0.5,  # Lower = more consistent, Higher = more creative
    "max_tokens": 1000,  # Increase for longer responses
    "top_p": 0.95,       # Can add nucleus sampling
    "frequency_penalty": 0.0,  # Penalize repeated tokens
}
```

---

## 📊 Monitoring & Troubleshooting

### Performance Monitoring

**Metrics to Track:**
- API response time (target: <5 seconds)
- Token usage efficiency
- Error rate
- User adoption rate

**Check Logs:**
```bash
# In Odoo logs, look for:
# - "pharmacy.ai.service"
# - "HF_API_TOKEN"
# - "AI service error"
```

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "Token not set" | API token missing | Configure HF_API_TOKEN in system parameters |
| "Connection timeout" | Network/API slow | Check internet, retry, verify API status |
| "Permission denied" | Wrong user group | Assign user to correct group |
| "Unexpected response" | Model behavior | Try rephrasing question, check API status |
| "Slow responses" | API congestion | Retry after delay, use during off-peak hours |

### Debug Mode

To enable verbose logging:

```python
# In models/pharmacy_ai_service.py
import logging
_logger = logging.getLogger(__name__)

# Add to _call_llm():
_logger.info(f"Sending request to Hugging Face API")
_logger.info(f"Message count: {len(messages)}")
_logger.info(f"Response time: {response.elapsed.total_seconds()}s")
```

---

## 📚 References

- **Hugging Face:** https://huggingface.co
- **Llama 3.1 Model:** https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
- **API Documentation:** https://huggingface.co/docs/api-inference/quicktour
- **Rate Limits:** Check Hugging Face account page for API limits

---

## 🎓 Examples & Recipes

### Recipe 1: Quality Monitoring Workflow

```
1. Daily: Collect customer feedback
2. Weekly: Analyze 20-30 feedback items using sentiment analysis
3. Process: Categorize by sentiment (Positive/Neutral/Negative)
4. Action: Review negative feedback for improvements
5. Report: Share trends with operations team
```

### Recipe 2: Chatbot Knowledge Base Expansion

```
1. Monitor common chatbot questions
2. Update system prompt with additional context
3. Add custom data methods for frequently asked topics
4. Test responses, iterate
5. Document Q&A patterns
```

### Recipe 3: Integration with Customer Portal

```
Future enhancement:
- Add sentiment analyzer to customer feedback form
- Auto-categorize feedback before submission
- Display sentiment-based alerts to managers
- Trigger auto-responses for negative feedback
```

---

## 📞 Support & Feedback

- Report issues via system administration
- Provide feedback on chatbot usefulness
- Share suggested improvements
- Document custom modifications for knowledge base

---

**Last Updated:** May 18, 2026  
**Version:** 1.1  
**Author:** Muhammad Qasim Shabbir

