from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def offer_accepted(self):
        if 'accepted' in self.property_id.offer_ids.mapped('status'):
            raise UserError("You cannot accept more than 1 offer for a single Property")
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def offer_refused(self):
        for record in self:
            record.status = 'refused'
        return True

    _check_negative_offer_price = models.Constraint('CHECK(price >= 0)',
                                                    "Have you ever thought of having negative value as an offer Price? Price can't be negative, check your Math!")
