from odoo import models, fields, api, exceptions
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offers"
    _unique = True
    _order = 'price desc, property_id desc'

    price = fields.Float("Price", readonly=False, required=True)
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
            ("pending", "Pending")
        ],
        default="pending",
        string="Status",
        required=True
    )

    partener_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    create_date = fields.Date(default=date.today())

    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    
    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = int((record.date_deadline - record.create_date).days)

    def set_offer_accepted(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partener_id
            record.property_id.state = 'offer_accepted'

    def set_offer_rejected(self):
        for record in self:
            record.status = 'rejected'
            # record.property_id.selling_price = 0

    # def set_offer_pending(self):
    #     for record in self:
    #         record.status = 'pending'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id']) #* self.env[target-model].browse(vals[related-field])

            if vals['price'] < property.best_price:
                raise exceptions.UserError('The new offer cannot be less than the best offer.')
            
            if property.state == 'new':
                property.state = 'offer_received'
        
        return super().create(vals_list)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price should be strictly positive.')
    ]