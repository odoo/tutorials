from odoo import fields,models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tags'
    _description = 'Model for Property tags such as "cozy","renovated", etc'

    name = fields.Char(required=True,string="")
