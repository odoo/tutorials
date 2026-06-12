# Chapter 7 — Relations Between Models

The property record links to type, buyer, salesperson, tags, and offers.

---

## New models added

- **Property Type** — `Many2one`, `ondelete='set null'`
- **Buyer** — `Many2one` → `res.partner`, `copy=False`, `ondelete='set null'`
- **Salesperson** — `Many2one` → `res.users`, `default=self.env.user`, `ondelete='set null'`
- **Tags** — `Many2many`, auto-creates junction table
- **Offers** — `One2many` (inverse of `property_id`), `ondelete='cascade'`, `_order = 'price desc'`, embedded inside property form with `editable="bottom"`

---

## Relation types

- **Many2one** = one column + one FK in DB
- **Many2many** = junction table (not optimization — relational DB necessity). Named `{t1}_{t2}_rel`
- **One2many** = virtual field, nothing in DB. Backed by child's Many2one

---

## What I learned extra

- **M2M junction table** — SQL can't store ID lists. Junction table is THE standard solution. Odoo auto-creates it.
- **`editable="bottom"`** on list → inline editing, no form view needed for simple models. Applied to both **Property Type** and **Tags** (both only have `name` field).
- **`open_form_view="True"`** — built-in list attribute (Odoo JS parses it), adds arrow column per row to open form view. Only works with `editable` also set. No Python code needed. Also applied to both Type and Tags.
- **`form_view_ref`** context key → controls which form opens for relational sub-items (used on `<field>`, NOT a list attribute)

---
