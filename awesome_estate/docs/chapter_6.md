# Chapter 6 - Basic Views

- Model file: `awesome_estate_property.py`
- View file: `awesome_estate_property_views.xml`
- Manifest file: `__manifest__.py`

The manifest loads the security file first and the views file after it.

---

## Odoo XML basics

- `<odoo>`: root tag of the XML file
- `<record>`: creates a database record
- `<field>`: sets a value on that record
- `model="ir.ui.view"`: this record is a view
- `arch`: XML layout of the view
- `type="xml"`: tells Odoo that `arch` is XML text

### View tags

- `<list>`: list view
- `<form>`: form view
- `<search>`: search view
- `<sheet>`: main form area
- `<group>`: field grouping
- `<notebook>`: tab container
- `<page>`: one tab inside a notebook

---

## Actions and menus

### Action
- XML ID: `awesome_estate_property_action`
- Model opened: `awesome.estate.property`
- View mode: `list,form`

An action tells Odoo which model to open and which views to use.

### Menus
Menu path:

- `Real Estate`
  - `Properties`
    - `Properties`

Menu IDs:

- `awesome_estate_root_menu`
- `awesome_estate_first_level_menu`
- `awesome_estate_property_menu`

The menu IDs are the technical names Odoo uses in XML.

### How actions and menus work

- `ir.actions.act_window` (e.g. `awesome_estate_property_action`) — opens the model
- `ir.ui.menu` (e.g. `awesome_estate_property_menu`) — adds the menu entry
- `ir.ui.view` (e.g. property list/form/search views) — defines the screen layout

---

## `ir.ui.view`

`ir.ui.view` is the Odoo model that stores view definitions in the database.

### `arch`
`arch` is the actual XML layout stored inside the view record.

### Example
A view record like:

```xml
<record id="awesome_estate_property_view_list" model="ir.ui.view">
```

means:
- create a database record
- store it as a view
- give it an XML ID so other XML can reference it

---

## Inheritance

If we want to change an existing view, we use inheritance.

- `inherit_id`: points to the original view
- `xpath`: updates part of the XML without replacing the full view

That is how Odoo extends views cleanly.

---

## List View attributes learned

### `editable`
- `"top"` or `"bottom"` — makes list inline-editable, skips form view
- Used on Property Type list (single field `name`, form view is overkill)
- Used on Offers tab inside Property form (`editable="bottom"`)
- Internally: `_editable_tag_list()` in `ir_ui_view.py` returns `True` when `editable` is set

### `form_view_ref`
- Context key (NOT `open_form_view`) — controls which form opens for relational fields
- `<field name="partner_id" context="{'form_view_ref': 'base.view_partner_form'}"/>`
- Read by `_get_view_refs()` and `_get_x2many_missing_view_archs()` in `ir_ui_view.py`

### Other common attributes
- `multi_edit="1"` — bulk editing
- `decoration-*` — conditional styling (bf=bold, danger=red, success=green, muted=grey)
- `create/delete/edit="0"` — hide buttons
- Field-level: `invisible`, `readonly`, `required`, `widget`, `sum`, `optional`

---

## What I learned

- Python defines the model
- XML defines the UI
- `ir.ui.view` stores the UI in the database
- `arch` is the XML layout
- actions open models
- menus make the model reachable
- XML IDs connect records together
- inheritance lets us modify an existing view instead of rewriting it
- `editable="bottom"` makes a list inline-editable, form view not needed for simple models

---

## Quick verify

```bash
community/odoo-bin -d patja --addons-path=community/addons,enterprise,tutorials -u awesome_estate --dev xml
