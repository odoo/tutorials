from odoo import fields, models  # type: ignore

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Ayve"
    _order = "name"

    #constraint name, definition of constraint, a display warning
    _sql_constraints = [
        (
            "unique_property_tag",
            "unique(name)",
            "A Property Tag with the same name already exists in the Database!"
        )
    ]

    name = fields.Char(required=True)
    