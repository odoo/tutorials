# How fields are converted to the database

- `fields.Char` → `varchar` if a size is set, otherwise `text`
- `fields.Text` → `text`
- `fields.Integer` → `int4` (PostgreSQL integer)
- `fields.Float` → `numeric` with precision, or `float8` if no digits are set
- `fields.Boolean` → `bool`
- `fields.Date` → `date`
- `fields.Datetime` → `timestamp` without timezone (UTC)
- `fields.Selection` → `varchar` (stores the internal key string)
- `fields.Many2one` → `int4` (foreign key)
- `fields.Binary` → `bytea` if not attachment-backed, otherwise stored in `ir.attachment`
- `fields.Html` → `text`
- `fields.Monetary` → `numeric` linked to a currency

---

## Blueprint, methods, and required fields

- `class` = blueprint
- `methods` = functions
- `required=True` translates to `NOT NULL` in SQL

---

## Module namespace vs business concept

- `awesome_estate` is the module namespace prefix
- `property` is the business concept inside that module

So the technical model name becomes `awesome_estate.property`.

---

## Selection: key vs label

- **Key** / internal value stored in the database
  - `"north"`, `"south"`, `"east"`, `"west"`

- **Label** / display value shown in the UI
  - `"North"`, `"South"`, `"East"`, `"West"`

---

## Chapter 3 verification

### 1) Upgrade or install the module
`/home/odoo/odoo19/community/odoo-bin -d patja --addons-path=community/addons,enterprise,tutorials -u awesome_estate --stop-after-init`

### 2) Check the table and columns
`psql -d patja -c "\pset pager off" -c "\d awesome_estate_property"`

### 3) Check `required=True` becomes `NOT NULL`
`psql -d patja -c "\pset pager off" -c "SELECT column_name, is_nullable FROM information_schema.columns WHERE table_name='awesome_estate_property' AND column_name IN ('name', 'expected_price');"`

You should see `is_nullable = NO` for `name` and `expected_price`.
