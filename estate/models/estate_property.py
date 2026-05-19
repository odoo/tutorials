from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "It's free real estate"

    # Order attributes
    _order = "id desc"
    
    name = fields.Char(required=True,)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        copy=False,)
    expected_price = fields.Float(required=True,)
    selling_price = fields.Float(readonly=True, copy=False,)
    bedrooms = fields.Integer(default=2,)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West'),],
        )
    state = fields.Selection(
            string='State',
            selection=[
                ('new', 'New'),
                ('offer_received', 'Offer Received'),
                ('offer_accepted', 'Offer Accepted'),
                ('sold', 'Sold'),
                ('canceled', 'Cancelled'),
            ],
            default='new',
            required=True,
            copy=False,
        )

    # Reserved fields
    active = fields.Boolean(default=True, string='Active',)

    # Relations
    property_type_id = fields.Many2one("estate.property.type",)
    property_tag_ids = fields.Many2many("estate.property.tag",)
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user,)
    buyer_id = fields.Many2one('res.partner', copy=False,)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers",)

    # -------------------------------------------------------------------------
    # COMPUTED FIELDS
    # -------------------------------------------------------------------------
    total_area = fields.Integer(
        string="Total Area (sqm)", 
        compute="_compute_total_area",
    )

    best_price = fields.Float(
        string="Best Offer", 
        compute="_compute_best_price",
    )

    # -------------------------------------------------------------------------
    # SQL Constraints
    # -------------------------------------------------------------------------
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', 
        'A property expected price must be strictly positive.',
    )
    
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)', 
        'A property selling price must be positive.',
    )

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------
    @api.depends("living_area", "garden_area",)
    def _compute_total_area(self,):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price",)
    def _compute_best_price(self,):
        for property in self:
            if property.offer_ids:
                property.best_price = max(property.offer_ids.mapped("price"), default=0.0)
            else:
                property.best_price = 0.0

    # -------------------------------------------------------------------------
    # CONSTRAINTs METHODS
    # -------------------------------------------------------------------------
    @api.constrains('expected_price', 'selling_price',)
    def _check_selling_price(self,):
        for property in self:
            # Selling price = 0 => Do nothing
            if float_is_zero(property.selling_price, precision_digits=2):
                continue

            minimum_price = property.expected_price * 0.90

            if float_compare(property.selling_price, minimum_price, precision_digits=2) < 0:
                raise UserError(self.env._("The selling price cannot be lower than 90% of the expected price."))

    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------
    @api.onchange("garden",)
    def _onchange_garden(self,):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # -------------------------------------------------------------------------
    # CRUD METHODS
    # -------------------------------------------------------------------------
    @api.ondelete(at_uninstall=False,)
    def _unlink_except_new_or_canceled(self,):
        for property in self:
            if property.state not in ('new', 'canceled',):
                raise UserError(self.env._("You can only delete properties that are New or Canceled."))

    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------
    def action_sold(self,):
        for property in self:
            if property.state == 'canceled':
                raise UserError(self.env._("You cannot sell a canceled property."))
        self.state = 'sold'
        return True

    def action_cancel(self,):
        for property in self:
            if property.state == 'sold':
                raise UserError(self.env._("You cannot cancel a sold property."))
        self.state = 'canceled'
        return True
