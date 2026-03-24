from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _inherit = ['estate.property.offer']
    _name = 'estate.property.offer'

    account_move_id = fields.Many2one('account.move', string="Invoice count")
