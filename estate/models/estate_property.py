from odoo import models, fields, api
from datetime import datetime, timedelta


class Property(models.Model):
    _name = 'estate.property' 
    _description = 'estate property model'

    postcode = fields.Char(required=True)
    date_availability = fields.Date(required=True, 
                                    copy=False, 
                                    default=lambda self: (datetime.now() + timedelta(days=3*30)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(required=True, default=0.0, copy=False)
    bedrooms = fields.Integer(required=True, default=2) 
    living_area = fields.Integer(required=True)
    facades = fields.Integer(required=True)
    garage = fields.Boolean(required=False)
    garden = fields.Boolean(required=False)
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'), 
            ('south', 'South'), 
            ('east', 'East'), 
            ('west', 'West'),
        ],
        string='Garden Orientation',
        default='north',
    )
    name = fields.Char(default='Uknown')
    last_seen = fields.Datetime('Last seen', default=fields.Datetime.now)
    state = fields.Selection(
        selection=[
                ('New', 'new'),
                ('Offer Received', 'offer_received'),
                ('Offer Accepted', 'offer_accepted'),
                ('Sold', 'sold'),
                ('Cancelled', 'cancelled')],
        default="New",
        string="state",
    )
    active = fields.Boolean(default=True)
    description = fields.Text(default="when duplicated status and date are not copied")

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False, default=None)
    salesperson_id = fields.Many2one('res.users', 
                                     string="Seller",
                                     default=lambda self: self.env.user)


    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price', string="Best Offer")


    def action_do_something(self):
        print('**** ACTION DO SOMETHING HAS BEEN CALLED ****')
        return True

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.0
    
    @api.onchange('garden')
    def _onchange_garden_values(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None
