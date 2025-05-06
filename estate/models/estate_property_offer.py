from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', required=True, string="Partner ID")
    property_id = fields.Many2one('estate.property', string="Property ID")
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(compute='_compute_total_days', inverse='_inverse_total_days', string='Deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True, string="Property Type")

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.depends('create_date', 'validity')
    def _compute_total_days(self):
        for record in self:
            record.date_deadline = fields.Date.add((record.create_date or fields.date.today()), days=record.validity)

    def _inverse_total_days(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days if record.date_deadline else 0

    def action_set_accepted(self):
        for record in self:
            property_rec = record.property_id
            if any(offer.status == "accepted" for offer in property_rec.offer_ids):
                raise UserError("An offer was already accepted for this property")

            record.status = "accepted"
            property_rec.update({
                'selling_price': record.price,
                'buyer_id': record.partner_id.id,
                'status': 'offer_accepted',
                })
            remaining_offers = property_rec.offer_ids.filtered(
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

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property = self.env["estate.property"].browse(val["property_id"])
            if property.status == "sold":
                raise UserError("You cannot create an offer for a sold property!")
            max_offer_price = max(property.offer_ids.mapped("price"), default=0.0)
            if val["price"] < max_offer_price:
                raise UserError("The offer must be higher than an existing offer!")
            property.status = "offer_received"
        return super().create(vals)
