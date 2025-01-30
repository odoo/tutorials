from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

from datetime import date, timedelta


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property"
    _order = "id desc"


    name = fields.Char('Property Name', required=True, translate=True)

    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        string="Date of Availability",
        copy=False,
        default=lambda self: date.today() + timedelta(days=30 * 3)
    )    
    expected_price = fields.Float('Expected Price')
    best_price = fields.Float('Best Price',compute="_compute_best_price",
        store=True)

    selling_price = fields.Float('Selling Price',readonly=True,copy=False)
    bedrooms = fields.Integer('Number of Bedrooms',default=2)
    living_area = fields.Integer('Living Area (in sq.m.)')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('Has Garage')
    garden = fields.Boolean('Has Garden')
    total_area = fields.Integer('total Area (in sq.m.)',compute="_compute_total",store=True)

    garden_area = fields.Integer('Garden Area (in sq.m.)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation")
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        string="State",
        required=True,
        copy=False,
        default='new'
    )

    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)
    
    property_type_id = fields.Many2one('estate_property_type', string="Property Type")
    seller_id = fields.Many2one('res.users', string="Seller")
    buyer_id = fields.Many2one('res.partner', string="Buyer",copy=False)    
    tag_ids = fields.Many2many('estate_property_tag', string="Property Tags")
    offer_ids = fields.One2many('estate_property_offer', 'property_id', string="Offers")


    offer_count = fields.Integer('Offer Count', compute='_compute_offer_count')



    @api.depends('offer_ids')

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price >= 0)',
        'A property expected price must be strictly positive'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)',
        'A property selling price must be strictly positive'),
        ('check_living_area_positive', 'CHECK(living_area >= 0)',
        'A property living area must be strictly positive'),
        ('check_garden_area_positive', 'CHECK(garden_area >= 0)',
        'A property garden area must be strictly positive'),
        ('check_total_area_positive', 'CHECK(total_area >= 0)',
        'A property total area must be strictly positive'),
        ('check_bedrooms_positive', 'CHECK(bedrooms >= 0)',
        'A property number of bedrooms must be strictly positive'),
        ('check_facades_positive', 'CHECK(facades >= 0)',
        'A property number of facades must be strictly positive'),
        ('check_sequence_positive', 'CHECK(sequence >= 0)',
        'A property sequence must be strictly positive'),
    ]

    
    @api.depends("garden_area","living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price') or [0.0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False


    def action_cancel(self):
        for record in self:
            print("record.state",record.state)
            if record.state == 'sold':
                raise UserError("A sold property cannot be canceled.")
            record.state = 'canceled'




    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("A canceled property cannot be marked as sold.")
            if not record.offer_ids.filtered(lambda offer: offer.status == 'accepted'):
                raise UserError("No accepted offer exists for this property.")
            accepted_offer = record.offer_ids.filtered(lambda offer: offer.status == 'accepted')[0]
            record.selling_price = accepted_offer.price
            record.buyer_id = accepted_offer.partner_id
            record.state = 'sold'
            print("hello")

    @api.constrains('expected_price','selling_price')
    def check_selling_expected(self):
        for record in self:
            if record.selling_price and record.selling_price>0  and record.expected_price:
                if record.selling_price < record.expected_price*.9:
                    raise ValidationError("The selling price cannot be lower than the expected price by 0.9.")
   


    def unlink(self):
        """Prevent deletion if state is not 'New' or 'Cancelled'."""
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(
                    "You can only delete properties in 'New' or 'Cancelled' state."
                )
        return super().unlink()
    

    
    def is_offer_accepted(self):
        return bool(self.offer_ids.filtered(lambda offer: offer.state == 'accepted'))
