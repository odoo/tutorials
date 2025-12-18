from odoo import api, fields, models
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property Offer"
    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date or fields.Datetime.now()
            ) + timedelta(days=record.validity)

    # @api.depends("create_date", "date_deadline") Not working right now!!!
    # def _inverse_date_deadline(self):
    #     print("Hello!")
    #     for record in self:
    #         record.validity = (
    #             (record.date_deadline or fields.Datetime.now())
    #             - (record.create_date or fields.Datetime.now())
    #         ).days
