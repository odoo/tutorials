from odoo import models, fields, api
from datetime import timedelta, date
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            today = record.create_date
            if today:
                today = record.create_date
            else:
                today = date.today()
            if record.validity:
                record.deadline = today + timedelta(days=record.validity)
            else:
                record.deadline = today

    def _inverse_deadline(self):
        for record in self:
            if record.deadline:
                # Convert create_date to a date object
                today = fields.Date.to_date(record.create_date)
                # Convert deadline to a date object
                deadline_date = fields.Date.from_string(record.deadline)
                record.validity = (deadline_date - today).days
            else:
                record.validity = 7  # Default to 7 if deadline is not set

    @api.depends('property_id')
    def action_status_accept(self):
        self.status = 'accepted'
        price_percent = (self.price / self.property_id.expected_price) * 100
        if price_percent > 90:
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
        else:
            raise ValidationError("The selling price must be at least 90%")

    def aciton_status_refused(self):
        self.status = 'refused'

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'The Price of Offer should be positive'),
    ]
