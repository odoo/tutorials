from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("waiting", "Waiting for approval"),
        ],
        default="waiting",
    )
    partner_id = fields.Many2one("res.partner")
    property_id = fields.Many2one("estate.property")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    validity = fields.Integer(default=7)
    property_state = fields.Selection(
        related="property_id.state", readonly=True, string="Property State"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True, readonly=False
    )

    _check_price = models.Constraint(
        "CHECK(price >= 0)", "The price can't be negative."
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                fields.Date.today(), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date)
            record.validity = (record.date_deadline - create_date).days

    def action_do_accept(self):
        for record in self:
            if record.property_id.state in ("offer_accepted", "sold"):
                raise UserError(self.env._("There is already an accepted offer."))
            # record.property_id.offer_ids.write({"state": "refused"})
            record.state = "accepted"
            record.property_id.state = "offer_accepted"
        return True

    def action_do_refuse(self):
        for record in self:
            if record.state == "accepted":
                offers = record.property_id.offer_ids.filtered(
                    lambda offer: offer.state == "waiting"
                )
                record.property_id.state = "offer_received" if offers else "new"
            record.state = "refused"
        return True

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env["estate.property"].browse(vals["property_id"])
            if prop.state in ("offer_accepted", "sold"):
                raise UserError(self.env._("There is already an accepted offer."))
            prop.state = "offer_received"
        return super().create(vals_list)
