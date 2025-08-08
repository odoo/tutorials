from datetime import timedelta 

from odoo import api, fields , models 
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property represents offers made by buyers on properties"
    _order = 'price desc'
    _sql_constraints = [
        ('check_offer_price', 
         'CHECK(price > 0)', 
         "The offer price must be strictly positive!")
    ]  

    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity", default=7)
    status = fields.Selection(
        string="Status",
        default='new',
        selection=[
            ('new', "New"),
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ]
    )
    date_deadline = fields.Date(
        string="Deadline Date",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True
    )  
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        related='property_id.property_type_id',
        store=True,
        string="Property Type",
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.selling_price:
                raise UserError("A selling price has already been set. You cannot accept another offer.")
            offer.status = 'accepted'
            offer.property_id.write({
                'state': 'offer_accepted',
                'selling_price': offer.price,
                'buyer_id': offer.partner_id.id,
            })
            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('id', '!=', offer.id)
            ])
            other_offers.write({'status': 'refused'})

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            new_offer = vals.get('price')
            if property_id:
                property = self.env['estate.property'].browse(property_id)
                existing_offer = self.search([('property_id.id', '=', property_id), ('price', '>=', new_offer)])
                if existing_offer:
                    raise UserError("You cannot create an offer with a lower or equal amount than an existing offer.")
                property.state = 'offer_received'
        return super(EstatePropertyOffer, self).create(vals_list)
