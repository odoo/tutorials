from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "an amount a potential buyer offers to the seller"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name="estate.property",
        required=True,
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    _check_positive_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer price must be positive!",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date or fields.Date.today()
            ) + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                record.date_deadline - fields.Date.to_date(record.create_date)
            ).days

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    def action_accept(self):
        for record in self:
            # TODO: property state should be readonly and just check on state == 'offer_accepted'
            if any(offer.status == 'accepted' for offer in record.property_id.offer_ids):
                raise UserError("Property already has another accepted offer.")
            # TODO: consider checking other property states
            record.status = "accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
