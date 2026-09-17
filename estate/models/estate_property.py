from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate property model'

#   Property information
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Availability', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    has_garage = fields.Boolean('Garage')
    has_garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West'),
        ]
    )
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'),
                   ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer accepted'),
                   ('sold', 'Sold'),
                   ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string='Property Type')

#   Other Information
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)

#   Tags
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

#   Offers
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
    best_price = fields.Float(compute='_compute_best_price', string='Best Offer')

#   Computation Fields:

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:  # QUESTION is the for each loop here necessary ? or can I just use self ?
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.

    @api.onchange('has_garden')
    def _onchange_has_garden(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

#   Actions buttons
    def action_cancel_property_state(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Cancelled properties cannot be cancelled again !')
            elif record.state == 'sold':
                raise UserError('Sold Properties cannot be cancelled !')
            record.state = 'cancelled'
            return True
        return True


    def action_sell_property_state(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold Properties cannot be sold again !')
            elif record.state == 'cancelled':
                raise UserError('Cancelled properties cannot be sold !')
            record.state = 'sold'
            return True
        return True

#   Actions :
    def action_set_selling_offer(self, buyer, price):
        for record in self:
            if record.buyer_id:
                raise UserError('An offer is already accepted for this house')
            record.buyer_id = buyer
            record.selling_price = price
            return True
        return True
