from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "These are Estate Module Property Types"
    _order = "name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The property type name must be unique"),
    ]

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(string="Properties", comodel_name="estate.property", inverse_name="property_type_id")
    sequence = fields.Integer(string="Sequence", default=10)
