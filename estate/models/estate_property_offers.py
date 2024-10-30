from odoo import fields, models, api
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError, UserError


class EstatePropertyOffers(models.Model):

    _name = "estate.property.offers"
    _description = "Estate Property Offers Model"
    _order = "price desc"

    price = fields.Float(string='Offer Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
       )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete='cascade')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store="True")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            best_offer = self.env['estate.property'].browse(vals['property_id']).best_price
            if vals['price'] < best_offer:
                raise UserError("You cannot create an offer with price lesser than %f" % best_offer)
            else:
                offer = super().create(vals_list)
                self.env['estate.property'].browse(vals['property_id']).state = 'offer received'
                return offer

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'An offer price must be strictly positive'),
    ]

    @api.constrains('status', 'property_id.selling_price')
    def _check_if_exsits_accepted_offer(self):
        for record in self:
            if record.property_id.selling_price > 0:
                raise ValidationError('You cannot accept multiple offers')
    
    # Methods
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(record.validity)
            else:
                record.date_deadline = datetime.today() + timedelta(record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7

    def action_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer accepted'

    def action_refused(self):
        for record in self:
            if record.status == 'accepted':
                record.status = "refused"
                record.property_id.selling_price = False
                record.property_id.buyer = False
            else:
                record.status = "refused"
