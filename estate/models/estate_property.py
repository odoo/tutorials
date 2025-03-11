from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(string="Property Name", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Date(string="Availability From", default=(fields.Date.today() + relativedelta(months=3)))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (in sqft)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (in sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        default='north',
    )
    state = fields.Selection(
        string="State",
        selection=[
            ('draft', "Draft"),
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        copy=False,
        default='new',
        tracking=True
    )
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company, required=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one('res.partner', string="Salesperson", default=lambda self: self.env.user, tracking=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False, tracking=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string="Property Offers"
    )
    total_area = fields.Float(compute='_compute_total_area', store=True)
    best_price = fields.Float(compute='_compute_best_price', store=True)
    image_1920 = fields.Image(string="Property Image", max_width=1920, max_height=1920)

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive.'),
        ('positive_selling_price', 'CHECK(selling_price > 0)', 'A property selling price must be positive.')
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
          for property in self:
            if (
                not float_is_zero(property.selling_price, precision_digits=2)
                and float_compare(property.selling_price, property.expected_price * 0.9,
                precision_digits=2) == -1
            ):
                raise ValidationError("Selling price must be at least 90% of the expected price!")
    
    def unlink(self):
        if any(property.state not in ['new', 'cancelled'] for property in self):
            raise UserError("You can not delete a property if it is not in 'new' or 'cancelled' state")
        return super(EstateProperty, self).unlink()

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
       for property in self:
          property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
       for property in self:
             property.best_price = max(property.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
       if self.garden:
          self.write({
              'garden_area': 10,
              'garden_orientation': 'north'
          })
       else:
         self.write({
             'garden_area': False,
             'garden_orientation': False
           })

    def action_cancel(self):
       for property in self:
            if property.state == 'sold':
                raise UserError("You cannot cancel a sold property!")
            elif property.state == 'cancelled':
                raise UserError("This property is already cancelled!")
            property.state = 'cancelled'

    def action_sold(self):
       for property in self:
            if property.state == 'cancel':
                raise UserError("You cannot sell a cancelled property!")
            elif property.state == 'sold':
                raise UserError("This property is already sold.")
            elif property.state != 'offer_accepted':
                raise UserError("There is no accepted offer on this property yet.")
            property.state = 'sold'

    def write(self, values):
        for property in self:
            if property.state in ['sold', 'cancelled'] and 'offer_ids' in values:
                raise UserError("You cannot add new offers to a sold or cancelled property.")
        return super(EstateProperty, self).write(values)
