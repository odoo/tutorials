from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection([
        ('contact', "Contact"),
        ('invoice', "Invoice Address"),
        ('delivery', "Delivery Address"),
        ('other', "Company Address")
    ], string="Address Type", default='contact')

    @api.model
    def create(self, vals):
        if 'parent_id' in vals and vals['parent_id']:
            vals['is_company'] = True
        return super(ResPartner, self).create(vals)
