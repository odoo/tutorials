from odoo import models,fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'for listing property types'

    name = fields.Char(string='Name',required=True)
