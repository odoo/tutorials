from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class PropertyOffers(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers that property has'
    _order = 'price desc'

    price = fields.Float(required=True)
    status = fields.Selection(
        selection = [
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline',  inverse="_inverse_date_deadline", string='Deadline')
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_constraints = [
        ('check_offer_price_positive', 
        'CHECK(price >= 0)', 
        'Offer price must be strictly positive.'),
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                count_validity = (record.date_deadline - record.create_date.date()).days
                if count_validity < 7:
                    raise UserError("Deadline cannot be set within 7 days")
                record.validity = count_validity

    def action_accept(self):
        self.property_id.offer_ids.status = 'rejected'
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = 'offer_accepted'

    def action_reject(self):
        for record in self:
            record.status = 'rejected'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if property_id.state != 'offer_received':
                property_id.state = 'offer_received'
            if property_id.offer_ids:
                # we have written _order = "price desc" in the model, so the first offer is the highest one
                if vals['price'] < property_id.offer_ids[0].price:
                    raise ValidationError("The offer price must be higher than the existing offer.")
        return super().create(vals_list)
