import datetime

from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "real estate property offer"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        help="The status determines if the offer has been accepted or refused",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inveres_date_deadline",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + datetime.timedelta(
                days=record.validity
            )

    def _inveres_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() or fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    def accept_offer(self):
        for record in self:
            property = record.property_id
            if property.state == "sold":
                raise exceptions.UserError("Property already sold")

            record.status = "accepted"
            property.state = "sold"
            property.selling_price = record.price
            property.buyer_id = record.partner_id
        return True

    def reject_offer(self):
        for record in self:
            if record.status == "accepted":
                raise exceptions.UserError("Offer has already been accepted")
            record.status = "refused"
        return True
