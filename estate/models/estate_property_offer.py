from odoo import api, models, fields, exceptions
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Offer Price", required=True)

    status = fields.Selection([
        ('accepted', "Accepted"),
        ('refused', "Refused")
    ], string="Status", copy=False)

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    create_date = fields.Date(default=fields.Date.today)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date
                record.validity = delta.days

    def action_accept(self):
        for record in self:
            if record.property_id.status == 'sold' or record.status == 'accepted':
                raise exceptions.UserError("This property is already sold.")

            record.status = 'accepted'
            record.property_id.status = 'sold'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
