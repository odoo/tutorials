from datetime import date, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline")

    _check_price = models.Constraint("CHECK(price > 0)", "Offer price must be strictly positive.")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date or date.today()
            record.date_deadline = start_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else date.today()
            date_dif = record.date_deadline - start_date
            record.validity = date_dif.days

    def action_accept_offer(self):
        for record in self:
            if any(offer.status == 'accepted' for offer in record.property_id.offer_ids):
                raise UserError("An offer for this property has already been accepted.")
            else:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
