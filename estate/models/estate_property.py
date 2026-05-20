from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "textext"

    name = fields.Char(required=True)
    description = fields.Text()
    property_type_id = fields.Many2one('estate.property.type')
    postcode = fields.Char()
    date_availability = fields.Date(string= "Available From", default=lambda self: fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default='new',
    )
    salesperson_id = fields.Many2one('res.users', string= "Salesman", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', index=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Integer(string="Total Area (sqm)", compute='_compute_total_area')
    best_price = fields.Float(string="Best Offer", compute='_compute_highest_offer')

    # SQL constraints
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "A property expected price must be strictly positive."
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        "A property selling price must be strictly positive."
    )

    # Compute and inverse methods
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_highest_offer(self):
        for property in self:
            prices = property.offer_ids.mapped('price')
            property.best_price = max(prices, default=0.0)

    # Constrains methods and onchange methods
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_digits=2):
                continue
                
            limit_price = property.expected_price * 0.9
            if float_compare(property.selling_price, limit_price, precision_digits=2) == -1:
                raise ValidationError(
                    self.env._("The selling price cannot be lower than 90% of the expected price!"
                ))

    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # CRUD methods
    @api.ondelete(at_uninstall=False)
    def _check_state(self):
        for property in self:
            if property.state not in ('new', 'cancel'):
                raise UserError("You cannot delete a property that is not New or Cancelled!")

    # Action methods
    def action_cancel(self):
            for property in self:
                if property.state == 'sold':
                    raise UserError("A sold property cannot be canceled.")
                property.state = 'cancelled'
            return True

    def action_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError("A canceled property cannot be set as sold.")
            property.state = 'sold'
        return True
                