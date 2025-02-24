from odoo import models,fields,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Estate Property"

    name = fields.Char("Property Name", required=True)
    active = fields.Boolean(default=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postal Code")
    date_availability = fields.Date("Availability Date", copy=False, default= lambda self: fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Number of bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    property_image = fields.Image(string="Property Image")
    garden_orientation = fields.Selection(string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ])
    state = fields.Selection(
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        required=True, copy=False, default="new"
    )
    color = fields.Integer(string='Color')
    #Relational Fields
    property_type_id = fields.Many2one('estate.property.type', string = 'Property Type')
    user_id = fields.Many2one('res.users',string='Salesman',default=lambda self: self.env.user, required=True)
    partner_id = fields.Many2one('res.partner',string='Buyer',readonly=True)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tag', readonly=False)
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    #computed Fields
    total_area = fields.Char(string='Total Area', compute='_total_area')
    best_offer = fields.Integer(string='Best Offer',compute='_best_offer')

    @api.depends('living_area','garden_area')
    def _total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.depends('offer_ids.price')
    def _best_offer(self):
        best_price = 0
        for price in self:
            if price.offer_ids:
                best_price = max(price.offer_ids.mapped('price'))
            price.best_offer = best_price
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10

    def action_sold_property(self):
        for record in self:
            if record.state == 'canceled':
                raise ValidationError("Canceled Property cannot be sold")
            if record.selling_price == 0:
                raise ValidationError("Please accept any offer incase you don't have create one")
            else:
                record.state = 'sold'
        return True

    def action_cancle_property(self):
        if self.state == 'sold':
            raise ValidationError("Sold property cannot be cancled")
        self.state = 'canceled'
        return True

    @api.constrains('expected_price','selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price*0.9 and record.selling_price != 0:
                raise ValidationError("Selling price must be at least 90% of the expected price, if you wish to make an offer you must reduce your price")

    def unlink(self):
        for record in self:
            if record.state  not in ['new', 'canceled']:
                raise ValidationError("Only new and canceled properties can be deleted.")
        return super().unlink()

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.')
    ]
