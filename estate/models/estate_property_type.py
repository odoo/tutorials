from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char('Property Type', required=True, translate=True)
    property_ids = fields.One2many(
        comodel_name="estate_property", 
        inverse_name="property_type_id", 
        string="Properties"
    )

    sequence = fields.Integer(string='Sequence', default=10)  # Add the sequence field
