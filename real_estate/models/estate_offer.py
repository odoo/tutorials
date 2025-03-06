from odoo import models, fields, api
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = fields.Date.today() + timedelta(days=record.validity)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7  
