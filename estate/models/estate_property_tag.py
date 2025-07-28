from odoo import models, fields  # type: ignore

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string='Tag Name', required=True)

    property_ids = fields.Many2many(comodel_name='estate.property', string='Properties')