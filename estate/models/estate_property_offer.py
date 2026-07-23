from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "realestate.properties.offer"
    _description = "Real estate property offer"

    price = fields.Float("Price")
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
