# Architecture

This document describes how the `pharma_control_center` addon is structured and how the main flows work.
odoo-tutorials/pharma_control_center/
│
├── data/
│   ├── demo_medicines.xml
│   └── demo_patients.xml
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CHANGELOG.md
│   ├── DEMO_DATA.md
│   ├── SECURITY.md
│   ├── TECHNICAL_DETAILS.md
│   └── USER_GUIDE.md
│
├── models/
│   ├── __init__.py
│   ├── pharma_control_center.py
│   ├── pharmacy_cart.py
│   ├── pharmacy_category.py
│   ├── pharmacy_interaction.py
│   ├── pharmacy_patient.py
│   ├── pharma_medicine.py
│   ├── pharmacy_ai_service.py
│   ├── pharmacy_chatbot.py
│   ├── privacy_terms.py
│   ├── sentiment_analysis_wizard.py
│   └── __pycache__/
│
├── security/
│   ├── groups.xml
│   ├── ir.model.access.csv
│   ├── pharmacy_patient_security.xml
│   ├── pharmacy_security.xml
│   └── sale_order_security.xml
│
├── tests/
│   └── (test files not shown)
│
├── views/
│   ├── pharma_control_center_views.xml
│   ├── pharmacy_cart_views.xml
│   ├── pharmacy_category_views.xml
│   ├── pharmacy_interaction_views.xml
│   ├── pharmacy_medicine_views.xml
│   ├── pharmacy_order_views.xml
│   ├── pharmacy_patient_views.xml
│   ├── sales_report_views.xml
│   ├── manager_analytics_views.xml
│   ├── ai_views.xml
│   └── privacy_terms_views.xml
│
├── __init__.py
├── __manifest__.py
├── README.md
└── __pycache__/
### Models

- `pharmacy.medicine`: medicine master data + custom stock + expiry logic
- `pharmacy.category`: medicine categories (parent/child hierarchy)
- `pharmacy.patient`: patient records linked to a doctor (`res.users`)
- `pharmacy.interaction`: interaction pairs used for cart warnings / blocking
- `pharmacy.cart` + `pharmacy.cart.line`: per-user cart and checkout logic
- `pharma.control.center`: dashboard/profile record

### Views / Menus

All menus live under the root menu **"💊 Your Pharma CC"**:

- **👤 User Dashboard**: `pharma.control.center` (form)
- **💊 Medicines**: `pharmacy.medicine` (kanban/list/form)
- **🛒 Order from Cart**: `pharmacy.cart` (form, filtered to the current user)
- **📄 Orders**: `sale.order` (list/form, restricted by record rules)
- **👥 Patients**: `pharmacy.patient` (doctor/manager only)
- **⚙️ Configuration → 📂 Categories**: `pharmacy.category` (manager only)
- **⚠️ Drug Interactions**: `pharmacy.interaction` (manager only)
- **📊 Analytics**: `sale.order` graph/pivot reporting (manager only)
- **🤖 AI Sentiment Analysis**: `sentiment.analysis.wizard` (manager only)
- **🤖 AI Assistant**: `pharmacy.chatbot` (all users)
- **🔒 Privacy Policy**: `privacy.terms` (all users)
- **📜 Terms of Service**: `privacy.terms` (all users)

## Key Business Flows

### 1) Add Medicine to Cart

Source: `models/pharma_medicine.py` (`pharmacy.medicine.add_to_cart`)

1. User sets `order_qty` on a medicine record.
2. The module finds (or creates) a `pharmacy.cart` for the current user.
3. A `pharmacy.cart.line` is created or updated for that medicine.

### 2) Cart Checkout

Source: `models/pharmacy_cart.py` (`pharmacy.cart.action_checkout`)

1. Validate cart is not empty.
2. Detect interactions between medicines in the cart:
   - Any interaction with severity `severe` blocks checkout.
3. For each cart line:
   - Ensure there is a linked `product.product` (created on demand).
   - Build `sale.order.line` values (quantity + unit price from the medicine).
4. Create a `sale.order` for the current user’s partner.
5. Confirm the sale order.
6. Create an invoice and post it.
7. Reduce `pharmacy.medicine.quantity` by the purchased quantities.
8. Clear the cart lines.

### 3) Dashboard Statistics

Source: `models/pharma_control_center.py`

The dashboard computes live KPIs by querying:
- `pharmacy.medicine` (counts, expiry buckets, stock totals/value)
- `sale.order.line` (today’s quantity and sales amount)
- `pharmacy.patient` (doctor’s assigned patients / all patients for managers)
