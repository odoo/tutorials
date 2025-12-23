from odoo import api, fields, models
from odoo.exceptions import UserError


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Offer Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date("Deadline", compute='_compute_date_deadline', inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related='property_id.property_type_id', string="Property Type", store=True, readonly=True)

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive"
    )

    @api.model
    def create(self, vals_list):
        for record in vals_list:
            property = self.env['estate.property'].browse(record["property_id"])
            min_price = min(offer.price for offer in property.offer_ids) if property.offer_ids else 0
            if record["price"] < min_price:
                raise UserError(self.env._(f"Offer must be greater than {min_price}"))
            property.status = "offer_received"

        return super().create(vals_list)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.status = "offer_accepted"

            # Reject other offers
            other_offers = record.property_id.offer_ids.filtered(lambda o: o.id != record.id)
            other_offers.action_reject_offer()

    def action_reject_offer(self):
        for record in self:
            record.status = "refused"
            if record.property_id.status == "offer_accepted" and record.property_id.buyer_id == record.partner_id:
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = False
                record.property_id.status = "offer_received"
