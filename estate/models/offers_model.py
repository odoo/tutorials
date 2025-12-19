from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta
from odoo.tools.float_utils import float_compare


class Offer(models.Model):
    _name = "estate.offers"
    _description = "Offers Model"

    price = fields.Integer(required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        required=False,
    )
    building_id = fields.Many2one("estate.buildings", string="Building")
    partner_id = fields.Many2one("res.partner", string="Partner")
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        for record in self:
            if record.status != "accepted" and record.building_id.state not in [
                "sold",
                "canceled",
            ]:
                record.status = "accepted"
                record.building_id.state = "offer accepted"
                record.building_id.buyer_id = record.partner_id
                record.building_id.value = record.price
                other_offers = self.search(
                    [
                        ("building_id", "=", record.building_id.id),
                        ("id", "!=", record.id),
                    ]
                )
                other_offers.write({"status": "refused"})
            elif record.building_id.state in ["sold", "canceled"]:
                raise UserError("Cannot accept offers for sold or canceled buildings.")
            else:
                raise UserError("Offer is already accepted.")

    def action_refuse_offer(self):
        for record in self:
            if record.status != "refused":
                record.status = "refused"
                record.building_id.state = "offer received"
                record.building_id.buyer_id = False
            else:
                raise UserError("Offer is already refused.")

    _price_positive_constraint = models.Constraint(
        "CHECK (price > 0)", "Offer price must be positive."
    )

    @api.constrains("building_id", "price")
    def _check_price(self):
        for record in self:
            if (
                float_compare(
                    0.9 * record.building_id.value, record.price, precision_digits=2
                )
                == 1
            ):
                raise UserError(
                    "Offer price must be at least 90% of the building's value."
                )
