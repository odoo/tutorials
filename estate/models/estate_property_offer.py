from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')])

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = date.today() + timedelta(days=offer.validity)
    
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = max(0, (offer.date_deadline - offer.create_date.date()).days)
            else:
                offer.validity = max(0, (offer.date_deadline - date.today()).days)

    def accept_offer(self):
        for offer in self:
            if offer.status == "Accepted":
                return True
            if len(list(filter(lambda order: order.status == "Accepted", offer.property_id.offer_ids))) > 0:
                raise UserError("You can't accept more than One offer by property")
            offer.status = "Accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
        return True

    def refuse_offer(self):
        for offer in self:
            offer.status = "Refused"
            offer.property_id.selling_price = 0
            offer.property_id.buyer_id = None
        return True