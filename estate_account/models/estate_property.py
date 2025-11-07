from odoo import fields, models


class EstateProperty(models.Model):
    _inherit="estate.property"
    
    def action_sold(self):
        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice'})
        return super().action_sold()
