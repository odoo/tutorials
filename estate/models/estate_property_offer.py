from odoo import fields, models, api
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    # Foreign keys
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            creation_date = record.create_date.date() or date.today()
            validity_time = timedelta(days=record.validity)
            record.date_deadline = creation_date + validity_time

    def _inverse_deadline(self):
        for record in self:
            creation_date = record.create_date.date() or date.today()
            validity_time = record.date_deadline - creation_date
            print("Setting validity to: " + str(validity_time))
            record.validity = validity_time.days

