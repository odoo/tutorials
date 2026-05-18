# Technical Details

This document is a code-oriented reference for the `pharma_control_center` addon.

## Core Models

### `pharmacy.medicine` (`models/pharma_medicine.py`)

Purpose: stores medicine master data, expiry logic, and a simple custom stock quantity.

Notable fields:
- Expiry: `expiry_date`, `days_to_expiry` (computed), `expiry_status` (computed: `fresh` / `expiring_soon` / `expired`)
- Stock: `quantity`, `reorder_level`, `need_reorder` (computed), `in_stock` (computed)
- Pricing: `price`, `cost_price`, `profit_margin` (computed)
- Cart helper: `order_qty` (used by `add_to_cart`)
- Licensing: `license_category` (`green` / `blue` / `white`)
- Sales integration: `product_id` (created on-demand by `_create_product()`)

Key methods:
- `add_to_cart()`: adds the current medicine to the current user’s cart.
- `_create_product()`: creates a `product.product` and links it to the medicine if missing.

Notes:
- `last_sale_order_id` and `last_invoice_id` exist on the model but are currently not updated by any code.

### `pharmacy.cart` and `pharmacy.cart.line` (`models/pharmacy_cart.py`)

Purpose: cart lines + totals + checkout orchestration.

Notable fields (cart):
- `cart_line_ids`: list of cart lines
- `total_quantity`, `total_amount`: computed from cart line subtotals
- `barcode_input`: input field used by `action_add_by_barcode()`
- `interaction_warnings`: computed text summary for interactions among medicines in the cart

Key methods (cart):
- `action_add_by_barcode()`: finds `pharmacy.medicine` by barcode and adds quantity 1.
- `action_add_quick_medicines()`: bulk-adds selected medicines at `quick_order_qty`.
- `action_checkout()`: creates a `sale.order`, creates & posts an invoice, reduces medicine stock, clears the cart.

Drug interaction behavior:
- Warnings are displayed when interactions exist between cart medicines.
- Checkout is blocked only when at least one interaction has `severity == 'severe'`.

### `pharma.control.center` (`models/pharma_control_center.py`)

Purpose: dashboard record + profile sync + computed KPIs.

Profile fields stored on the dashboard:
- `display_name`, `email`, `phone`, `avatar`

Sync behavior:
- On create/write the module syncs profile values to the linked `res.users` and `res.partner`.

Computed KPIs (non-stored):
- Medicine KPIs: totals, stock value, low/out-of-stock, expiring soon, expired
- Patient KPIs: total patients, “my patients” (for doctors)
- Today’s order KPIs: quantity and subtotal for today’s `sale.order.line`

### `pharmacy.patient` (`models/pharmacy_patient.py`)

Purpose: patient data with a required `doctor_id` assignment.

Notable constraints:
- SQL constraint on `email` to keep it unique.

### `pharmacy.interaction` (`models/pharmacy_interaction.py`)

Purpose: defines an interaction between two medicines with `severity` and `warning_text`.

## AI & Chatbot Integration

### `pharmacy.ai.service` (`models/pharmacy_ai_service.py`) – AbstractModel

Purpose: provides AI/LLM integration using Hugging Face API and Llama 3.1-8B model.

**Configuration:**
- Requires system parameter `HF_API_TOKEN` (Hugging Face API token)
- Uses `https://router.huggingface.co/v1/chat/completions` endpoint
- Model: `meta-llama/Llama-3.1-8B-Instruct:novita` (configurable in `_call_llm`)
- Temperature: 0.7, Max tokens: 500

Key methods:
- `_call_llm(messages, model)`: sends message list to Hugging Face API, returns response text
- `analyze_sentiment(text)`: returns sentiment classification (Positive/Neutral/Negative)
- `chat(user_message, conversation_history)`: context-aware chatbot response with live data injection
- `_get_medicine_stock_info(user_message)`: extracts medicine name and returns stock info
- `_get_today_orders_info(user_message)`: fetches today's order statistics when relevant

### `pharmacy.chatbot` (`models/pharmacy_chatbot.py`) – TransientModel

Purpose: provides access point for AI pharmacy assistant with conversational interface.

Notable fields:
- `chat_history`: accumulated conversation history (text, readonly)
- `user_message`: user input field (not required)

Key methods:
- `action_send_message()`: sends user message to AI service, appends response to chat history, returns updated form

Features:
- Maintains persistent chat history in same session
- Displays emoji indicators (🧑‍⚕️ for user, 🤖 for AI)
- Provides context-aware responses using live pharmacy data
- Accessible via modal dialog

### `sentiment.analysis.wizard` (`models/sentiment_analysis_wizard.py`) – TransientModel

Purpose: one-shot sentiment analysis tool for customer feedback (manager access).

Notable fields:
- `feedback_text`: required input field for customer feedback
- `sentiment_result`: readonly field for analyzed sentiment

Key methods:
- `action_analyze()`: calls `pharmacy.ai.service.analyze_sentiment()`, returns updated form

Features:
- AI analyzes feedback and returns: Positive, Neutral, or Negative
- Manager-only access for quality monitoring
- Simple wizard interface for quick analysis

### `privacy.terms` (`models/privacy_terms.py`) – TransientModel

Purpose: placeholder model for privacy policy and terms of service views (no data fields).

Features:
- Lightweight transient model
- Views display comprehensive policies
- Accessible to all authenticated users
- Two separate forms: Privacy Policy and Terms of Service

## Checkout Implementation Notes

- The module uses a *custom* stock quantity field (`pharmacy.medicine.quantity`).
- Checkout reduces that field directly (it does not use the Inventory/Stock app).
- The module creates a `product.product` for each medicine on first checkout, and uses that product in `sale.order.line`.
- After order confirmation, the module creates and posts an invoice automatically.

