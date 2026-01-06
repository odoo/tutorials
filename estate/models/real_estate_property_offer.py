from odoo import exceptions, api, fields, models
from dateutil.relativedelta import relativedelta


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float()
    _offer_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be positive.'
    )
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("real_estate", string="Property", required=True)
    validity = fields.Integer(string="Validity(days)", default=7)
    deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_validity"
        )

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.deadline = date + relativedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            record.validity = ((record.deadline) - record.create_date.date()).days

    def accept_offer(self):
        for record in self:
            if record.property_id.buyer_id:
                raise exceptions.UserError("Only One Offer can be accepted")
            else:
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.status = "accepted"
        return True

    def reject_offer(self):
        for record in self:
            if record.property_id.buyer_id and record.status == "accepted":
                raise exceptions.UserError("Accepted Offer can not be rejected")
            else:
                record.status = "refused"
        return True
