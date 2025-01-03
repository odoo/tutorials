from odoo import models, fields, api
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offers"

    price = fields.Float("Price", readonly=False, required=True)
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("pending", "Pending")
        ],
        default="pending",
        string="Status",
        required=True
    )

    partener_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")

    create_date = fields.Date(default=date.today())

    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    
    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(self.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = int((record.date_deadline - record.create_date).days)