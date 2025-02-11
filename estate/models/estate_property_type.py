from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is the model for the estate property type"
    _order = "name"


    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id", string="Property")
    sequence = fields.Integer(string="Sequence", default=1, help="Used to order types")

    _sql_constraints = [
        ("unique_property_type", "UNIQUE(name)", "The same property type is already exist")
    ]
