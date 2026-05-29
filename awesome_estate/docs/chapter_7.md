# Chapter 7 - Relations Between Models

- Created `awesome.estate.property.type`
- Added the property type list/form/action/menu
- Imported the new model in `models/__init__.py`
- Loaded the new XML in `__manifest__.py`
- Added ACL access for the new model in `security/ir.model.access.csv`
- Added `property_type_id` on `awesome.estate.property`


- `Many2one` means "one thing points to one other thing"
- A property can have one type
- Many properties can share the same type

Example:
- Property: `Villa 12`
- Property type: `Villa`

So `property_type_id` is like a pointer from a property to its type.

# Notes

- `Many2one` links one record to one record
- `property_type_id` stores the chosen type for each property
- In the UI, you can pick the type from a dropdown
- Odoo saves that choice in the database, so the property remembers its type

### Database record example

The property type model becomes a database table record in Odoo, for example:

- model: `awesome.estate.property.type`
- database row fields: `name = "House"` or `name = "Apartment"`

The list/form/action/menu XML also becomes database records in:

- `ir.ui.view`
- `ir.actions.act_window`
- `ir.ui.menu`

### Why the new field matters

When you add `property_type_id` to `awesome.estate.property`, each property can point to one of those property type records.

