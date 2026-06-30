from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "model for estate property types"
    name = fields.Char(required=True)
    # tag_ids = fields.One2many("estate.property.tag","property_type_id",string="Tags")
