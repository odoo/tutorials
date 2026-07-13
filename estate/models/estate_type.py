from odoo import models, fields


class EstateType(models.Model):
    _name = 'estate.type'
    _description = 'Estate Type'

    name = fields.Char(string='Name', required=True)
