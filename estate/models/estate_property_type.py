from odoo import models, fields # type: ignore

class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is property Type table."

    name = fields.Char(required=True)
    active = fields.Boolean(Default=False)
    number = fields.Integer()




