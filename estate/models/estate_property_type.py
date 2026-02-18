from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type model"
    _check_name = models.Constraint("unique(name)", "Property type must be unique")
    _order = "sequence,name"

    name = fields.Char("Name", required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    sequence = fields.Integer("Sequence", default=1, help="used to order by sequence")
