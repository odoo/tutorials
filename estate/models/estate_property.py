from odoo import api, fields, models

import datetime

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property of the estate"

    name = fields.Char('Name', required=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', required=True)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    best_offer = fields.Float('Best Offer', readonly=True, compute='_compute_best_offer')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date', copy=False, default=lambda _: fields.Date.today()+datetime.timedelta(days=90))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('west', 'West'),
            ('south', 'South'),
            ('east', 'East'),
        ]
    )
    total_area = fields.Integer('Total Area', compute='_compute_total_area', readonly=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
    )

    active = fields.Boolean('Active', default=True)

    def action_set_cancelled(self):
        self.write({'state': 'cancelled'})
    
    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price') + [0])
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

