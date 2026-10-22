from datetime import timedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    validity = fields.Integer(string="Validity Duration", default=7)
    date_deadline = fields.Date(
        string="Validity Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Buyer", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", string="Property")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = start_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start_date).days
