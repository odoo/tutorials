from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.tools import float_compare
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
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        copy=False,
        default='new',
        tracking=True,
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one('res.partner', string="Salesperson", tracking=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False, tracking=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string="Property Offers",
    )
    total_area = fields.Float(compute='_compute_total_area', store=True)
    best_price = fields.Float(compute='_compute_best_price', store=True)
    image_1920 = fields.Image(string="Property Image", max_width=1920, max_height=1920)

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive.'),
        ('positive_selling_price', 'CHECK(selling_price > 0)', 'A property selling price must be positive.'),
    ]

    @api.model
    def ondelete(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise UserError(f"Cannot delete property in state '{property.state}'. It can only be deleted if it is 'New' or 'Cancelled'.")

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
       for property in self:
          if float_compare(property.selling_price, 0.0, precision_digits=2) == 0 and not property.offer_ids.filtered(lambda offer: offer.state == 'offer accepted'):
              continue
          if float_compare(property.selling_price, property.expected_price * 0.9, precision_digits=2) < 0:
               raise ValidationError(
                 ("The selling price cannot be lower than 90 percentage of the expected price. Expected Price: %.2f, Selling Price: %.2f") %
                 (property.expected_price, property.selling_price)
                )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
       for property in self:
          property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
       for property in self:
          if property.offer_ids:
             property.best_price = max(property.offer_ids.mapped('price'))
          else:
             property.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
       if self.garden:
          self.garden_area = 10
          self.garden_orientation = 'north'
       else:
          self.garden_area = False
          self.garden_orientation = False

    def action_cancel(self):
       for property in self:
            if property.state == 'sold':
                raise UserError("You cannot cancel a sold property!")
            if property.state == 'cancelled':
                raise UserError("This property is already cancelled!")
            property.state = 'cancelled'

    def action_sold(self):
       for property in self:
            if property.state == 'cancel':
                raise UserError("You cannot sell a cancelled property!")
            if property.state == 'sold':
                raise UserError("This property is already sold.")
            # Check if there are any offers on the property before marking it as sold
            offers = self.env['estate.property.offer'].search([('property_id', '=', property.id), ('status', '=', 'accepted')])
            if not offers:
                raise UserError("The property can not be sold as there are no offers accepted.")
            property.state = 'sold'

    @api.model
    def action_change_state(self, new_state):
        for property in self:
            if property.state == new_state:
                return
            property.state = new_state

    def rating_get_partner_id(self):
        return self.partner_id
