# Contact Product Categories – Market View Report

## Overview

The **Market View Report** is an analytical feature of the `contact_product_categories` module that helps evaluate **market coverage and demand gaps** by correlating:

- Companies (contacts)
- Their business/product categories
- Relevant products (including multi-category products)
- Estimated demand vs. actual monthly sales

The report is **read-only**, **SQL-based**, and designed for **sales planning and strategic analysis**, not transactional workflows.

---

## Business Problem

Companies often operate in multiple business areas (e.g. *Broiler*, *Feed Mill*), while products may belong to multiple categories.  
Standard Odoo reports do not clearly answer:

> *Which products are relevant for this company’s business, and how much potential demand exists compared to actual sales?*

The Market View Report solves this by linking **companies and products via category hierarchies**, not manual product assignments.

---

## Key Concepts

### Company Business Categories
- Companies (`res.partner`) can be linked to one or more **product categories**
- These categories represent the company’s **business scope**

### Product Categories
- Products (`product.template`) may have:
  - one **main category**
  - multiple **extra categories**
- Category hierarchy (parent/child) is respected

---

## What the Report Shows

Each row represents a unique combination of:

**Company × Business Category × Product**

For each row, the report provides:

| Field | Description |
|------|------------|
| Company | Business partner |
| Business Category | One of the company’s assigned categories |
| Product | Product matching that category |
| Dosage per ton | Product usage factor |
| Capacity (tons) | Company production capacity |
| Potential Monthly Demand | Capacity × dosage |
| Monthly Result | Actual sold quantity (current month) |
| Demand Difference | Potential − actual |
| Sales Manager | Last salesperson who sold this product to the company |

---

## Matching Logic

A product is included in the report **if any of its categories**:

- matches a company business category, **or**
- is a child of that category (via hierarchy)

This means:
- Multi-category products are fully supported
- Products may appear under **multiple business categories** for the same company (by design)

---

## Technical Implementation

### Architecture
- Implemented as a **PostgreSQL SQL VIEW**
- Exposed via an Odoo model with `_auto = False`
- No ORM loops or computed Python logic

### Why SQL View?
- High performance on large datasets
- Deterministic results
- Correct handling of many-to-many category relationships
- Easy aggregation and grouping

---

## Data Sources

| Model | Purpose |
|------|--------|
| `res.partner` | Companies and capacity |
| `res_partner_product_category_rel` | Company → business categories |
| `product.template` | Products and dosage |
| `product_template_extra_category_rel` | Extra product categories |
| `product.category` | Category hierarchy |
| `sale.order` / `sale.order.line` | Monthly sales data |
| `product.product` | Variant → template mapping |

---

## Limitations / Design Decisions

- Report is **read-only**
- Uses **current month** sales only
- A product may appear multiple times if it matches multiple business categories
- Not intended for transactional operations (quotes, orders, etc.)

---

## Typical Use Cases

- Market coverage analysis
- Identifying **unsold but relevant products**
- Demand gap analysis
- Sales planning and prioritization
- Account and territory reviews

---


---

## Summary

The Market View Report provides a **category-driven analytical layer** that connects companies, products, and sales to highlight **market potential vs. actual performance**, enabling more informed and targeted sales decisions.
