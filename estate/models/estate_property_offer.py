from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers that propeties receive."
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    _sql_constraints = [
        ("positive_offer_price", "CHECK(price > 0)", "Offer Price Must be Positive")
    ]

    @api.depends("property_id.create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.property_id.create_date + relativedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = date.today() + relativedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.property_id.create_date:
                record.validity = (
                    record.date_deadline - record.property_id.create_date.date()
                ).days
            else:
                record.validity = 7

    def action_accept_offer(self):
        self.write({"status": "accepted"})
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        return True

    def action_refuse_offer(self):
        self.write({"status": "refused"})
        return True

    @api.model
    def create(self, vals):
        property_id = self.env["estate.property"].browse(vals["property_id"])
        property_id.state = "offer received"
        if any(offer.price > vals.get("price", 0) for offer in property_id.offer_ids):
            raise UserError(
                _(
                    "You cannot create an offer with a lower price than an existing offer."
                )
            )
        return super().create(vals)
