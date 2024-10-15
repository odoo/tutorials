from odoo import fields, models  # type: ignore

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Ayve"
    _order = "name"
    _sql_constraints = [
        (
            "unique_property_type",
            "unique(name)",
            "A Property Type with the same name already exists in the Database!"
        )
    ]


    name = fields.Char(required=True)
    property_id = fields.One2many('estate.property',"property_type_id", string="Property")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    