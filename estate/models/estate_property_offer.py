from odoo import api, fields, models
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity(Days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("validity", "date_deadline")
    def _compute_date_deadline(self):
        for record in self:
            creation_date = fields.Date.today() or record.create_date()
            record.date_deadline = timedelta(days=record.validity) + creation_date

    def _inverse_date_deadline(self):
        for record in self:
            creation_date = fields.Date.today() or record.create_date()
            date_diff = record.date_deadline - creation_date
            record.validity = date_diff.days
