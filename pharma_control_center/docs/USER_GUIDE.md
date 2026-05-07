# User Guide

This is a short functional guide for the backend menus provided by **Pharma Control Center**.

## Setup (Users & Roles)

1. Go to **Settings → Users & Companies → Users**
2. Open a user and assign one of:
   - **Pharma Control Center / Patient**
   - **Pharma Control Center / Doctor**
   - **Pharma Control Center / Manager**

## Medicines

Menu: **💊 Your Pharma CC → 💊 Medicines**

- Browse medicines in kanban/list.
- Open a medicine to view details like expiry status, stock quantity, and pricing.
- To add to cart:
  1. Set **Quantity to Order**
  2. Click **Add to Cart**

## Cart & Checkout

Menu: **💊 Your Pharma CC → 🛒 Order from Cart**

You can add items by:
- Scanning/typing a barcode (adds quantity 1), or
- Selecting medicines in **Add Medicines** and choosing a quantity.

The cart displays:
- Current cart lines with subtotals
- Total quantity and total amount
- Interaction warnings (if configured)

Checkout:
- Click **Complete the order**
- The module creates a Sales Order and a Customer Invoice, posts the invoice, reduces medicine stock, and clears the cart.

## Orders

Menu: **💊 Your Pharma CC → 📄 Orders**

Shows Sales Orders created through the checkout flow.

## Patients (Doctor / Manager)

Menu: **💊 Your Pharma CC → 👥 Patients**

- Doctors manage patient records assigned to them.
- Managers can manage all patients.

## Drug Interactions (Manager)

Menu: **💊 Your Pharma CC → ⚠️ Drug Interactions**

Create interaction records by selecting:
- Medicine A
- Medicine B
- Severity (Minor/Moderate/Severe)
- Warning text

The cart will display warnings when interaction pairs are present.
Checkout is blocked when any interaction in the cart is **Severe**.

## Dashboard

Menu: **💊 Your Pharma CC → 👤 User Dashboard**

- Update your profile (name/email/phone/avatar)
- View live KPIs for medicines and today’s orders

Doctors and managers also have a **My Patients** tab on the dashboard.

## Analytics (Manager)

Menu: **💊 Your Pharma CC → 📊 Analytics**

Provides graph/pivot reporting over Sales Orders.

