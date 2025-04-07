from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', required=True , string="Partner ID")
    property_id = fields.Many2one('estate.property', string="Property ID")
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(compute='_compute_total_days', inverse='_inverse_total_days', string='Deadline')

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]


    @api.depends('create_date','validity')
    def _compute_total_days(self):
        for record in self:
            record.date_deadline = fields.Date.add((record.create_date or fields.date.today()), days=record.validity)

    def _inverse_total_days(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days if record.date_deadline else 0

    def action_set_accepted(self):
        for record in self:
            if any([offer.status == "accepted" for offer in record.property_id.offer_ids]):
                raise UserError("An offer was already accepted for this property")

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.status = "offer_accepted"

            remaining_offers = record.property_id.offer_ids.filtered(
                lambda offer: offer.id != record.id
            )
            remaining_offers.write({"status": "refused"})

    def action_set_refused(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = False
            record.status = "refused"
        return True
