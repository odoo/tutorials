from odoo import models,fields


class EstatePropertyTag(models.Model):
    _name='estate.property.tag'
    _description="Estate Property Tag"

    name=fields.Char()
    property_ids = fields.Many2many('estate.property')
    