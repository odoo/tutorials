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

---

## Model types


- `Model` is the normal table-backed model
- `TransientModel` is for temporary  records
- `AbstractModel` is for shared base logic

### `AbstractModel` in more detail

An abstract model is like a reusable blueprint.

It is useful when I want to share fields or methods across multiple models, but I do not want Odoo to create a normal business table for it.

So:

- it is meant for code reuse
- it can be inherited by real models
- it is not the place where final business records live
- it helps keep common logic in one place instead of copy-pasting it

### `TransientModel` in more detail

`TransientModel` is still stored in the database, but Odoo cleans it up automatically.

It uses a vacuum process that removes old rows based on age or count limits.

From the code, I learned:

- old  records are deleted automatically
- cleanup runs through the transient vacuum logic
- records older than the allowed age can be removed
- if too many rows exist, Odoo also removes the oldest ones
- this is why wizard data does not stay around forever

That is why wizards feel temporary, even though they are real records while they exist.
