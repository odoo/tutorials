from datetime import timedelta
from odoo import api, exceptions,fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = 'price desc'

    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection([
        ('accepted', "Accepted"),
        ('refused', "Refused")
    ], string="Status", copy=False)
    create_date = fields.Date(default=fields.Date.today)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True, string="Property Type")

    _sql_constraints = [('check_offer_price', 'CHECK(price >= 0)', 'The offer price must be positive.')]

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

    def action_accept_offer(self):
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

    def action_refuse_offer(self):
        for record in self:
            if record.property_id.status == 'sold':
                raise exceptions.UserError("This property is already sold.")

            if record.property_id.status == 'cancelled':
                raise exceptions.UserError("This property is cancelled.")

            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            property_id = self.env["estate.property"].browse(record["property_id"])
            if record['price'] < property_id.best_price:
                raise exceptions.UserError(f"The offer must be higher than {property_id.best_price:.2f}.")
            property_id.status = 'offer_received'
        return super().create(vals_list)
