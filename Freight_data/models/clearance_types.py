from odoo import models, fields

class ClearanceTypes(models.Model):
    _name = 'clearance.types'
    _description = 'Clearance Types'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
