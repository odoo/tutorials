from odoo import fields, models

class EstatePorpertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for Estate Poperty'

    price = fields.Float()
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Estate Property", required=True)
