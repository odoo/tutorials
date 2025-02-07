from odoo import models, fields


class estate_property_type(models.Model):
    _name = "estate_property.type"
    _description = "estate property type"
    _order = "sequence, name asc"

    name = fields.Char("name", required=True)
    property_ids = fields.One2many('estate_property','property_type_id')
    sequence = fields.Integer('Sequence', default=1)


    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "The property type name must be unique!")
    ]
