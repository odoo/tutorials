from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Name"

    name = fields.Char('Property name', required = True, size = 30)
    selling_price = fields.Integer('Selling Price',
        readonly = True,
        copy = False,
        default = 1000000
    )
    description = fields.Char('Property description', size = 50)
    postcode = fields.Char('Postcode', size = 6)
    date_availability = fields.Date(
        default=fields.Date.today() + timedelta(days = 90), copy = False
    )
    expected_price = fields.Float('Expected price', required = True)
    bedrooms = fields.Integer('Bedrooms', default = 2)
    living_area = fields.Integer('Area')
    facades = fields.Integer('facade')
    garage = fields.Boolean('Available',
        default = False,
        help = 'Mark if Garage is available'
    )
    garden = fields.Boolean('Garden',
        default = False,
        help = 'Mark if Garden is Present',
    )
    garden_area = fields.Integer('Garden Area(sqm)', default = 0)
    active = fields.Boolean('Active',
        default = True,
        help = 'Mark if you want it as Active'
    )
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')]
    )
    state = fields.Selection(
        string = "Status",
        required = True,
        default = "new",
        copy = False,
        selection = [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )

    salesman_id = fields.Many2one('res.users',default = lambda self: self.env.user, string = 'Salesman')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=  True)
    tags_ids = fields.Many2many('estate.property.tags', string ='Tags')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string = "Offers")

    total_area = fields.Float(compute = '_compute_total_area', string = 'Total area(sqm)', store = True)
    best_price = fields.Float(compute = '_compute_best_offer', string = 'Best Offer', store = True)


    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
            self.total_area = self.living_area + self.garden_area
            return self.total_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_canceled(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            elif record.state == 'sold':
                raise UserError('It cannot be canceled once sold')
            elif record.state == 'cancelled':
                raise UserError('It is already canceled')
            return True

    def action_set_sold(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            elif record.state == 'cancelled':
                raise UserError('It cannot be sold once cancelled')
            elif record.state == 'sold':
                raise UserError('It is already sold')

