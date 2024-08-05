from odoo import models,fields


class estate_property_offer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property offer"

    price = fields.Float()
    status = fields.Selection(copy=False , selection=[('accepted', 'Accepted'),('refused','Refused')])
    partner_id = fields.Many2one("res.partner",required=True)
    property_id = fields.Many2one("estate_property",required=True)