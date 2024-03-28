from odoo import api, fields, models
from odoo.tools import relativedelta
from odoo.exceptions import UserError
from odoo.tools.translate import _

from .. import util


class OfferEstate(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for a property"
    _order = "price desc"

    _sql_constraints = [
        ("check_price", "check(price > 0)", "An offer's price must be strictly positive"),
    ]

    price = fields.Float("Price")
    status = fields.Selection(string="Status", copy=False, selection=[
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ])

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", related="property_id.property_type_id", store=True)

    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.write({
                "date_deadline": record.create_date.date() + relativedelta(days=record.validity),
            })

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.write({
                    "validity": (record.date_deadline - record.create_date.date()).days,
                })

    @api.model
    def create(self, vals):
        property_id = self.env["estate.property"].browse(vals["property_id"])
        if property_id.exists() and property_id.state == "new":
            property_id.write({"state": "offer_received"})
        return super().create(vals)

    @util.action
    def action_set_accepted(self):
        for record in self:
            if record.status == "accepted":
                continue

            property_id = record.property_id

            if "accepted" in property_id.offer_ids.mapped("status"):
                raise UserError(_("Only one offer can be accepted"))

            property_id.register_accepted_offer(record.partner_id, record.price)
            record.write({"status": "accepted"})

    @util.action
    def action_set_refused(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.write({"selling_price": 0.})

        self.write({"status": "refused"})
