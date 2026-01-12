from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _check_offer_price = models.Constraint(
        "CHECK(price>=0)", "Offer Price must be strictly positive"
    )
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity(Days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    disable_buttons = fields.Boolean(compute="_disable_offer_buttons", default=False)

    @api.depends("validity", "date_deadline")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                creation_date = record.create_date.date()
            else:
                creation_date = fields.Date.today()
            record.date_deadline = timedelta(days=record.validity) + creation_date

    @api.depends("property_id.offer_ids.status")
    def _disable_offer_buttons(self):
        for record in self:
            record.disable_buttons = "accepted" in record.property_id.offer_ids.mapped(
                "status"
            )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                creation_date = record.create_date.date()
            else:
                creation_date = fields.Date.today()
            date_diff = record.date_deadline - creation_date
            record.validity = date_diff.days

    def refuse_offer_action_icon(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("You cant refuse an already accepted offer")
            record.status = "refused"
        return True

    def accept_offer_action_icon(self):
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                raise UserError("An Offer has already been accepted for this offer")

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
            record.property_id.buyer_id = record.partner_id
        return True
