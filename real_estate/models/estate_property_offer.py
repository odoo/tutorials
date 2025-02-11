from datetime import date, timedelta
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = "Offers on Property"
    _order = 'price desc'

    create_date = fields.Date(
        string="Create Date",
        default=date.today(),
        readonly=True
    )
    price = fields.Float(
        string="Offer Price"
    )
    status = fields.Selection(
        selection = [
            ('accepted', "Accepted"),
            ('refused', "Accepted")
        ],
        string="Status",
        copy=False
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Buyer",
        required=True
    )
    property_id = fields.Many2one(
        comodel_name='estate.property',
        string="Property",
        required=True
    )
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string="Property Type",
        related='property_id.property_type_id'
    )

    date_deadline = fields.Date(
        string="Deadline Date",
        compute='_compute_date_deadline', 
        inverse='_inverse_date_deadline', 
    )
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date).days
            elif offer.date_deadline:
                offer.validity = 7

    def action_accept_offer(self):
        for offer in self:
            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'

    # SQL CONSTRAINTS   
    _sql_constraints = [
        (
            'check_offer_price',
            'CHECK(price>0)',
            'Offer Price must be positive'
        )
    ] 
