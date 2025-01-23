from odoo import fields, models

class offer(models.Model):
    _name = 'estate.house_offer'

    price = fields.Float()
    status = fields.Selection(selection=[('Accepted','Accepted'),('Refused','Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', stirng='Partner', required=True)
    property_id = fields.Many2one('house', 'Property applied on', required=True)