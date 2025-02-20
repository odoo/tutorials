from odoo import fields, models, api, exceptions
from odoo.tools import float_is_zero, float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    
    
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(copy=False, default=fields.Datetime.add(fields.Datetime.now(), months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        help="What is the orientation of the facade of the property"
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'), 
            ('offer-received', 'Offer received'), 
            ('offer-accepted', 'Offer accepted'), 
            ('sold', 'Sold'), 
            ('cancelled', 'Cancelled')
        ],
        required=True,
        copy=False,
        default='new'
    )

    property_type_id = fields.Many2one("estate.property.type", string="Type")
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False) 
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_total_area", readonly=True)

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
    

    best_price = fields.Float(compute="_compute_best_price", readonly=True)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0


    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden is True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sell_property(self):
        if self.state == 'cancelled':
            raise exceptions.UserError("Canceled properties cannot be sold.")
        else:
            self.state = 'sold'
    
    def cancel_property(self):
        if self.state == 'sold':
            raise exceptions.UserError("Sold properties cannot be cancelled.")
        else:
            self.state = 'cancelled'
    

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)',
         'The expected price of a property must be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price of a property must be positive.')
    ]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=1):
                return
            min_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_price, precision_digits=1) == -1:
                raise exceptions.ValidationError("The selling price is too low.")
