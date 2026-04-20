from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(string="name", required=True)
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Property Type",
    )
    sequence = fields.Integer("Sequence", default=1)

    _name_check = models.Constraint("UNIQUE (name)", "Please add unique type")
