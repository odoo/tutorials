from odoo import models, fields


class Vessel(models.Model):
    _name = 'vessel'
    _description = 'Vessel'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    vessel_owner = fields.Many2one('res.partner', string='Vessel Owner')
    status = fields.Boolean('Status', default=True)
