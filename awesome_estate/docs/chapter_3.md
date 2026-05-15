# How are fields converted to DB?

- `fields.Char` → varchar (if size set) or text
- `fields.Text` → text
- `fields.Integer` → int4 (PostgreSQL integer)
- `fields.Float` → numeric (with precision) or float8 (if no digits)
- `fields.Boolean` → bool
- `fields.Date` → date
- `fields.Datetime` → timestamp (without timezone — UTC)
- `fields.Selection` → varchar (stores the internal key string)
- `fields.Many2one` → int4 (foreign key)
- `fields.Binary` → bytea (if not attachment) or stored in `ir.attachment`
- `fields.Html` → text
- `fields.Monetary` → numeric (linked to a currency)

---

## Blueprint / methods / required

- `class` = blueprint
- `methods` = functions
- `required=True` translates to `NOT NULL` in SQL

---

## Module namespace vs business concept

- `awesome_estate` is the `__module__` namespace (a conventional prefix)
- `property` is the business concept inside that module

So the technical model name becomes: `awesome_estate.property`

---

## Selection: key vs label

- __key__ / internal value (stored in DB)
  - `"north"`, `"south"`, `"east"`, `"west"`

- __label__ / display value (shown in UI)
  - `"North"`, `"South"`, `"East"`, `"West"`
