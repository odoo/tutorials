# Security / Roles

This addon defines custom groups, model access rights (ACLs), and record rules under `security/`.

## API Configuration

### Hugging Face API Token

The chatbot and sentiment analysis features require a Hugging Face API token.

**Setup:**
1. Obtain a free token from [huggingface.co](https://huggingface.co/settings/tokens)
2. In Odoo, go to **Settings → Technical → Parameters → System Parameters**
3. Create a new parameter:
   - **Key:** `HF_API_TOKEN`
   - **Value:** Your Hugging Face API token
   - **Save**

**Error handling:** If the token is not configured, users will see: "HF_API_TOKEN not set in system parameters."

## Groups

Defined in `security/groups.xml`:
- `pharma_control_center.group_pharmacy_patient` (Patient)
- `pharma_control_center.group_pharmacy_doctor` (Doctor)
- `pharma_control_center.group_pharmacy_manager` (Manager)

All three groups currently imply `account.group_account_invoice` (invoice access).

## Record Rules (ir.rule)

### Medicines (`pharmacy.medicine`)
Defined in `security/pharmacy_security.xml`:
- Patient: only `license_category = white`
- Doctor: only `license_category in (blue, white)`
- Manager: no rule in this addon (sees all medicines)

### Patients (`pharmacy.patient`)
Defined in `security/pharmacy_patient_security.xml`:
- Doctor: only patients where `doctor_id = current user` (delete is not granted by the rule)
- Manager: all patients

### Sales Orders (`sale.order`)
Defined in `security/sale_order_security.xml`:
- Patient: only orders created by the current user
- Doctor: only orders created by the current user
- Manager: all orders

## Model Access Rights (ACL)

Defined in `security/ir.model.access.csv`.

Important notes:
- Odoo ACLs are **additive** across all groups a user belongs to. If a user has broad permissions from another group, that can widen access beyond what you expect.
- This addon currently includes several `base.group_user` ACL entries (full CRUD) for custom models. If you want strict Patient/Doctor separation, review and tighten these ACLs.

## UI-Level Restrictions

Some views/menus are restricted using `groups="..."` or view attributes (`create="false"`, `edit="false"`, `delete="false"`). These help with the user experience, but they are not a replacement for properly configured ACLs/record rules.

## AI & Chatbot Access Control

**AI Assistant Chatbot (pharmacy.chatbot)**
- All authenticated users (`base.group_user`) can access
- Available via menu: **🤖 AI Assistant**
- No role-based restrictions
- Requires valid `HF_API_TOKEN` in system parameters

**Sentiment Analysis (sentiment.analysis.wizard)**
- Managers only (`pharma_control_center.group_pharmacy_manager`)
- Available via menu: **🤖 AI Sentiment Analysis**
- For customer feedback quality monitoring
- Requires valid `HF_API_TOKEN` in system parameters

**Privacy Policy & Terms of Service (privacy.terms)**
- All authenticated users (`base.group_user`) can access
- Available via menus: **🔒 Privacy Policy** and **📜 Terms of Service**
- Read-only informational views
- No API requirements

