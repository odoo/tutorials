from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


from odoo import api, _, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "realestate.properties.offer"
    _description = "Real estate property offer"

    price = fields.Float("Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    validity = fields.Integer(
        "Validaty (days)",
        default=7,
    )
    date_deadline = fields.Date(
        "Deadline",
        compute="_computed_date_deadline",
        inverse="_inverse_validity_period",
        readonly=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("realestate.properties", required=True)

    @api.depends("validity")
    def _computed_date_deadline(self):
        for offer in self:
            create_date = offer.create_date if offer.create_date else datetime.today()
            if offer.validity:
                offer.date_deadline = create_date + timedelta(
                    days=offer.validity,
                )

    def _inverse_validity_period(self):
        for offer in self:
            create_date = offer.create_date if offer.create_date else datetime.today()
            offer.validity = (offer.date_deadline - create_date.date()).days

    def action_confirm(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise exceptions.UserError(_("One offer has already been accepted."))
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

    def action_cancel(self):
        for offer in self:
            offer.status = "refused"
            offer.property_id.selling_price = 0
            offer.property_id.buyer_id = None
