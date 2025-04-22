from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ], copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    date_deadline = fields.Date(string="Deadline Date",
                                compute="_compute_date_deadline",
                                inverse="_inverse_date_deadline")
    validity = fields.Integer(string="Validity Days", default=7)

    _sql_constraints = [
        (
            "check_price_positive",
            "CHECK(price >= 0)",
            "Offer price must be strictly positive.",
        ),
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for val in self:
            val.date_deadline = datetime.now() + relativedelta(days=val.validity)

    def _inverse_date_deadline(self):
        for val in self:
            if val.create_date and val.date_deadline:
                val.validity = (
                        val.date_deadline - val.create_date.date()
                ).days
            else:
                val.validity = 7

    def action_accept(self):
        for val in self:
            self.property_id.offer_ids.filtered(
                lambda x: x.status == "accepted").write({
                'status': "refused",
            })

            val.status = 'accepted'
            val.property_id.write({
                'buyer_id': val.partner_id.id,
                'selling_price': val.price,
            })

    def action_refuse(self):
        for val in self:
            val.status = 'refused'
            val.property_id.write({
                'buyer_id': False,
                'selling_price': False,
            })
