from odoo.tools.date_utils import add
from odoo.exceptions import UserError
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer model"

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = add(base_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            if record.date_deadline and base_date:
                record.validity = (record.date_deadline - base_date).days

    def accept_offer(self):
        for record in self:

            if record.status == "accepted":
                continue

            accepted_offer = record.property_id.offer_ids.filtered(lambda offer: offer.status == "accepted")
            if accepted_offer:
                raise UserError("Only one offer can be accepted for a giver property !")
            else:
                record.status = "accepted"
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
        return True

    def refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True

    _offer_price_strictly_positive_constraint = models.Constraint(
        "CHECK(price > 0)",
        "The price of an offer should be strictly greater than 0!"
    )
