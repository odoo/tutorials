from odoo import models, fields

class EstateType(models.Model):
    _name = "estate.property.type"

    name = fields.Char(string="Name", required=True)

    # estate_property_id = fields.One2many(
    #     comodel_name="estate.property",
    #     inverse_name="estate_property_type_id",
    #     string="Properties"
    # )
    