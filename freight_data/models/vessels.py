from odoo import models, fields


class Vessels(models.Model):
    _name = "vessels"
    _description = "Vessels"

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    vessel_owner_id = fields.Many2one('res.partner', string='Vessel Owner', required=True)
    status = fields.Boolean(string='Status', default=True)
