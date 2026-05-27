# Chapter 7 - Relations Between Models

- Created `awesome.estate.property.type`
- Added the property type list/form/action/menu
- Imported the new model in `models/__init__.py`
- Loaded the new XML in `__manifest__.py`
- Added ACL access for the new model in `security/ir.model.access.csv`

# Notes

- `Many2one` links one record to one record

### Database record example

The property type model becomes a database table record in Odoo, for example:

- model: `awesome.estate.property.type`
- database row fields: `name = "House"` or `name = "Apartment"`

The list/form/action/menu XML also becomes database records in:

- `ir.ui.view`
- `ir.actions.act_window`
- `ir.ui.menu`

So this chapter starts by creating a new relational model and exposing it in the UI.
