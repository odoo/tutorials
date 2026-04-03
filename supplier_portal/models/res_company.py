from odoo import api, models, fields


class ResCompany(models.Model):
    _name = 'res.company'
    _description = 'portal model'
    _inherit = 'res.company'

    # partner_id = fields.Many2one('res.partner',tracking=3)
    supplier_partner_ids = fields.Many2many(
        'res.partner',
        'partner_company_rel',
        'company_id',
        'partner_id',
        string='Suppliers',
    )
