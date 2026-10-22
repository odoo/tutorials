from datetime import timedelta

from odoo import api, fields, models, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    state = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    validity = fields.Integer(string="Validity Duration", default=7)
    date_deadline = fields.Date(
        string="Validity Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Buyer", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", string="Property")

    _check_offer_price = models.Constraint(
        'CHECK(price >= 0)',
        'Offer price must be greater than zero.'
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = start_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start_date).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state in ["sold", "cancelled", "accepted"]:
                raise exceptions.UserError("You cannot accept an offer for a sold, cancelled, or already accepted property.")

            record.state = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "accepted"

    def action_refuse_offer(self):
        for record in self:
            record.state = "refused"