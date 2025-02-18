from odoo import api,fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class EstatePropertyOffers(models.Model):
    _name = 'estate.property.offers'
    _description = 'Real estate property offers'
    _order = 'price desc'
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', "The offered price must be greater then 0."),
    ]

    price = fields.Float(string="Price")
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id')
    validity_days = fields.Integer(string="Valid till")
    deadline = fields.Date(
        compute='_compute_deadline',
        inverse='_inverse_deadline',
        store=True,
    )
    state = fields.Selection(
        string="Offer State",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ], 
        copy=False,
    )

    # Computes deadline using validity days
    @api.depends("validity_days")
    def _compute_deadline(self):
        for record in self:
            if record.validity_days:
                record.deadline = fields.Date.today() + timedelta(days=record.validity_days)

    # Let's user select manually as well.
    @api.depends("validity_days")
    def _inverse_deadline(self):
        for record in self:
            if record.validity_days:
                record.deadline = fields.Date.today() - timedelta(days=record.validity_days)

    # Sets offer state to accepted when called
    def action_offer_confirm(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda offer: offer.state == 'accepted'):
                raise UserError("You can't accept two offers!")
            
            record.write({'state': 'accepted'})  
            record.property_id.write({  
                'state': 'accepted',  
                'selling_price': record.price  
            })  

    # Sets offer state to refused when called
    def action_offer_cancel(self):
        for record in self:
            record.write({'state' : 'refused'})

    # Chnage the state of property to offer recevied when offer is created 
    @api._model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            property_id = val.get('property_id')
            offer_price = val.get('price')
            if property_id and offer_price:
                property = self.env['estate.property'].browse(property_id)
                offered_price = property.offer_ids.mapped('price')
                
                if offered_price and offer_price < max(offered_price):
                    raise ValidationError("You cannot create an offer lower than an existing one.")
                
                property.write({'state' :'received'})
        return super().create(vals_list)
