from odoo import api, models, fields, exceptions
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = 'price desc'

    price = fields.Float(string="Offer Price", required=True)

    status = fields.Selection([
        ('accepted', "Accepted"),
        ('refused', "Refused")
    ], string="Status", copy=False)

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True, string="Property Type")

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
            if record.property_id.status == 'sold':
                raise exceptions.UserError("This property is already sold.")

            if record.property_id.status == 'cancelled':
                raise exceptions.UserError("This property is cancelled.")

            existing_accepted_offer = record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
            if existing_accepted_offer:
                raise exceptions.UserError("Another offer has already been accepted for this property.")

            record.status = 'accepted'
            record.property_id.status = 'offer_accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.status == 'sold':
                raise exceptions.UserError("This property is already sold.")

            if record.property_id.status == 'cancelled':
                raise exceptions.UserError("This property is cancelled.")

            if not record.property_id.status == 'offer_accepted':
                record.property_id.status = 'offer_received'
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0
            record.status = 'refused'
        return True

    _sql_constraints = [('check_offer_price', 'CHECK(price >= 0)', 'The offer price must be positive.')]
