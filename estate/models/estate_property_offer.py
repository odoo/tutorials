from odoo import models, api, fields
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ('pending', 'Pending'),
    ])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(default=7, string="Validity (Days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline Date")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                # create_date = fields.Date.from_string(record.create_date)
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False  # Fallback for records not yet created

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                # create_date = fields.Date.from_string(record.create_date)
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = 0  # Reset if no date is set
