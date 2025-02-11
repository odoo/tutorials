from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name desc"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id")

    # === SQL Constraints === #
    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property type must be unique'),
    ]
