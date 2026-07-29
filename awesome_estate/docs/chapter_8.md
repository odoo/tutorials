# Chapter 8 — Computed Fields, Onchanges, and Inverse Functions

- Import change: `from odoo import api, fields, models` (added `api`)
- New fields on `awesome.estate.property`: `total_area`, `squared_area`, `best_price`
- New fields on `awesome.estate.property.offer`: `validity`, `date_deadline`

---

## Computed fields

A computed field's value is calculated by Python, not typed by the user.

```python
total_area = fields.Integer(compute='_compute_total_area', store=True)

@api.depends('living_area', 'garden_area')
def _compute_total_area(self):
    for record in self:
        record.total_area = record.living_area + record.garden_area

squared_area = fields.Integer(compute='_compute_squared_area', store=True)

@api.depends('living_area', 'garden_area', 'total_area')
def _compute_squared_area(self):
    for record in self:
        record.squared_area = record.total_area ** 2

best_price = fields.Float(compute='_compute_best_price', store=True)

@api.depends('offer_ids.price')
def _compute_best_price(self):
    for record in self:
        record.best_price = max(record.offer_ids.mapped('price'), default=0.0)
```

### `store=True`
- Creates a real database column. Search filters and sorting need a column.
- Exception: don't use when value depends on current user/time/context.

### `@api.depends`
- Lists every field used in the method body. Missing one = silent stale data.
- Works through relations: `@api.depends('offer_ids.price')` tracks price changes on linked offers.

`squared_area` depends on `total_area`, which itself is a computed field. Both must have `store=True` for the cascade to work in SQL.

---

## onchange vs depends

The form view updates `total_area` when you change `living_area` whether you use onchange or depends. The difference shows up when you sort, filter, or duplicate.

- `@api.onchange` only fires in the browser form. When records are created or modified through `write()` or `create()`, onchange never runs. It is form-only.
- `@api.depends` fires on ANY write. The ORM checks the dependency tree and recomputes automatically — form, import, server action, all of them.

---

## `mapped()` — extracting field values from relations

```python
# CORRECT: 1 line, Odoo standard
max(record.offer_ids.mapped('price'), default=0.0)

# WRONG: 6-line Python loop
prices = []
for offer in record.offer_ids:
    prices.append(offer.price)
if prices:
    record.best_price = max(prices)
```

`default=0.0` handles empty offer lists safely (`max([])` would crash).

---

## Inverse function — two-way computed fields

```python
date_deadline = fields.Date(
    compute='_compute_date_deadline',  # Forward: validity → date
    inverse='_inverse_date_deadline',  # Backward: date → validity
)
```

Without inverse, computed fields are read-only. With inverse, the user can edit either direction:
- Set validity=14 → deadline = today + 14
- Set deadline=2026-07-01 → validity = days until July 1

### Critical: `create_date` is None at creation

```python
if record.create_date:
    record.date_deadline = fields.Date.add(
        fields.Date.to_date(record.create_date), days=record.validity)
else:
    record.date_deadline = fields.Date.add(
        fields.Date.today(), days=record.validity)
```

Same guard in inverse. Without this, `None + 7 days` crashes.

---

## `@api.onchange` — UI-only, never business logic

```python
@api.onchange('garden')
def _onchange_garden(self):
    if self.garden:
        self.garden_area = 10
        self.garden_orientation = 'north'
    else:
        self.garden_area = 0
        self.garden_orientation = False
```

- Only fires in the browser form view.
- `self` is a single record — NO `for record in self:` loop.
- Garden is correct because it is a UI hint, not a business rule.

---

## What I learned

- `@api.depends` fires on ANY write. `@api.onchange` fires only in browser form.
- `store=True` creates a DB column. Without it, sort and filter silently do nothing.
- `squared_area` depends on `total_area`, which is also computed — chain works when both have `store=True`.
- `mapped()` extracts field values in one line instead of a Python loop.
- `inverse=` makes a computed field editable in both directions.
- `create_date` is `None` for unsaved records — guard with `today()` fallback.

---

## Review tasks — issues found and fixed

### Off-track items (fixed now)

| # | Issue | File | Fix applied? |
|---|-------|------|-------------|
| 1 | `squared_area` `@api.depends` missing `total_area` | `awesome_estate_property.py` | Added `'total_area'` to depends |
| 2 | `best_price` filter needed adding | `awesome_estate_property_views.xml` | Added filter to search view (works with `store=True`) |
| 3 | No `_rec_name` defined | `awesome_estate_property.py` | Works (defaults to `'name'`) but add for clarity |

### View additions (done)

| # | What | File |
|---|------|------|
| 1 | Added `squared_area` and `total_area` to list view columns | `awesome_estate_property_views.xml` |
| 2 | Added `squared_area` to form view (right column, under total_area) | `awesome_estate_property_views.xml` |

### Future review items (chapters 9+)

| Chapter | What to watch for | Pattern to use |
|---------|------------------|----------------|
| 9 | Button methods | `action_` prefix, `self.ensure_one()`, `UserError` for workflow blocks |
| 9 | Offer price escalation | `@api.model_create_multi`, `self.search([...])` not `filtered()` |
| 10 | Constraints | `models.Constraint` (SQL) for single-field checks, `@api.constrains` only for cross-field |
| 10 | Float comparisons | `float_compare()` from `odoo.tools.float_utils`, never `==` |
| 11 | UI decorations | `decoration-*` on list rows, `widget="statusbar"` on state |
| 12 | Deletion guards | `@api.ondelete(at_uninstall=False)`, not overriding `unlink()` |
