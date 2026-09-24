from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate_property.offer"
    _description = "Offer to the Estate"
    _order = "price desc"

    name = fields.Char("Nom", required=True)
    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)

    validity = fields.Integer("Validity")
    date_deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            base_date = (
                record.create_date if record.create_date else fields.Date.today()
            )
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def accept_offer_action(self):
        for record in self:
            if record.status == "refused":
                raise UserError("Refused offer cannot be acceptd")
            for properties in record.property_id:
                properties.accept_property_offer_action(record.partner_id, record.price)
            record.status = "accepted"
        return True

    def refuse_offer_action(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("Accepted offer cannot be refused")
            record.status = "refused"
        return True

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The Offer Price should be strictuly positive",
    )
