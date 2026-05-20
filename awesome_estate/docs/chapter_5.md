# Chapter 5 - First UI

## Action and Menus
- **Action (`ir.actions.act_window`)**: Connects a model to the UI, specifying view modes like `list,form`.
- **Menu Hierarchy**: 3 levels deep: Root Menu -> First Level Menu -> Action Menu.
- **Manifest Order**: XML files containing these UI definitions must be added to `__manifest__.py` under `data`. Data is loaded sequentially!

## Field Attributes
- `required=True`: Field cannot be empty. Translates to `NOT NULL` in the DB.
- `copy=False`: Prevents the field value from duplicating when a user clicks the "Duplicate" action on a record. Used for unique or situational data like `date_availability` or `selling_price`.
- `readonly=True`: Makes the field uneditable from the UI. E.g., `selling_price` updates programmatically when an offer is accepted, not by manual entry.

## Default Values
- Pre-populates a field logically when "New" is clicked.
- Can be a literal (`default=2`) or evaluated via an anonymous function.
- **Why use `lambda self:` for logic?**: If you say `default=date.today()`, Python computes it *once* when the Odoo server boots. Using `lambda self: date.today() + relativedelta(months=3)` evaluates dynamically at the *exact moment* the record is created.

## Reserved Fields
- **`active`**: Special boolean field. If `False`, the record is "Archived" and automatically hidden from standard searches (without deleting DB row).
- **`state`**: Selection field commonly used to drive business flow (e.g., New -> Offer Received -> Sold).

## Python / Odoo Conventions
- **String quotes (`''` vs `""`)**: Mechanically identical in Python. By Odoo / PEP 8 convention, use single quotes `''` for internal strings (keys, backend values) and double quotes `""` for UI text or docstrings.

## Selection Fields
Are lists of tuples acting as Key/Value pairs: `('north', 'North')`
- **Key (`'north'`)**: Backend identifier. Lower-case, internal logic, stored in DB.
- **Label (`'North'`)**: UI string. Shown to the user, can be translated easily.

## Date Imports
- `datetime.date`: Native module for server calendar dates (`date.today()`).
- `dateutil.relativedelta`: Robust utility that cleanly handles calendar leaps when calculating logic like `months=3`. Other periods supported: `years`, `months`, `weeks`, `days`, `hours`.

## Implementation Proof
All rules required by the Chapter 5 tutorial (readonly/copy overrides, dynamic default date, correctly formatted status options, active field implementation) have been applied exactly to specification in `awesome_estate_property.py`.

## Developer Setup Notes (`--dev`)
When executing and testing UI/view creations regularly, use the backend server command flag `--dev=all`. It auto-reloads your codebase so you bypass server restarts.
```bash
./odoo-bin -d patja -u awesome_estate --dev=all
```
**Common `--dev=` parameters:**
- `all`: Enables all developer configurations below.
- `reload`: Automatically bounces the python worker when Python code changes are detected.
- `qweb`: Forces QWeb templates/XML to read directly from disks instead of reading from the database caching engine. Highly recommended when editing views!
- `werkzeug`: Routes exceptions natively to the debug interactive debugger.
- `xml`: Validates XML files are structurally whole before trying to push them to PostgreSQL.

