from odoo import api, models, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _description = 'portal model'
    _inherit = 'res.partner'

    # parent_ids = fields.One2many('res.company','partner_id',tracking=3)
    allowed_company_ids = fields.Many2many(
        'res.company',
        'partner_company_rel',
        'partner_id',
        'company_id',
        string='Allowed Companies',
    )
