from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offers"
    _order = 'price desc'
    _sql_constraints = [
        ('check_price', 'CHECK(price >0)', 'The Offer Price must be strickly Positive.')
    ]

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ('accepted',"Accepted"),
            ('refused',"Refuesd")
        ]
    )
    partner_id = fields.Many2one('res.partner',string="Partner", required=True)
    property_id = fields.Many2one('estate.property',string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Date Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True
    )
    create_date = fields.Date(default=fields.Date.context_today)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type",
        related='property_id.property_type_id'
    )

    # compute date deadline from create date plus validity.
    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = (offer.create_date + timedelta(days=offer.validity))
            else:
                offer.date_deadline = False

    # inverse method to compute validity from create date and deadline
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date).days
            else:
                offer.validity = 7
                
    # action to check if any offer accepted then shows error
    # else change state to accepted and change selling price
    def action_accept(self):
        for offer in self:
            if offer.property_id.offer_ids.filtered(lambda x: x.status == 'accepted'):
                raise UserError("Only one offer can accepted.")
            
            offer.write({'status': 'accepted'})
            offer.property_id.write({
                'selling_price': offer.price,
                'buyer_id': offer.partner_id,
            })
    # action to change offer status to refused
    def action_refuse(self):
        self.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            offer_amount = vals.get('price')

            if property_id and offer_amount:
                property = self.env['estate.property'].browse(property_id)
                existing_offers = property.offer_ids.mapped('price')

                if existing_offers and offer_amount < max(existing_offers):
                    raise ValidationError(
                        "You cannot create an offer lower than an existing one."
                    )

                property.write({'state': 'received'})
        return super().create(vals_list)    
