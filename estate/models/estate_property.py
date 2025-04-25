from odoo import exceptions, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate model"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self: fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Allows to know where the sun is about the home")
    active = fields.Boolean(default=True)
    state = fields.Selection(string="Status",
                             required=True,
                             copy=False,
                             default="new",
                             selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                                        ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])
    total_area = fields.Integer(string="Total area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    # Many2One relationships
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    # Many2Many relationships
    tag_ids = fields.Many2many('estate.property.tag')

    # One2Many relionships
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    # -----------
    # Constraints
    # -----------

    _sql_constraints = [
        ('expected_price_constraint', 'CHECK(expected_price > 0)',
         'Your expected price must be positive.'),
        ('selling_price_constraint', 'CHECK(selling_price >= 0)',
         'Your selling price must be positive.')
    ]

    @api.ondelete(at_uninstall=False)
    def _check_property_state_to_delete(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError('An offer which is not "New" or "Cancelled" cannot be deleted...')

    @api.onchange('selling_price', 'expected_price')
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            is_selling_price_over_90_percent = float_compare(record.selling_price, 0.9 * record.expected_price, precision_rounding=1)
            if record.selling_price > 0 and is_selling_price_over_90_percent < 0:
                raise ValidationError("This selling price is under 90% of the expected price. Please review the expected price or the amount of the buyer's offer")

    # ---------------
    # Compute methods
    # ---------------

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max([0] + record.offer_ids.mapped('price'))  # To get 0 as best price if no offer

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # --------------
    # Public methods
    # --------------

    def action_cancel_offer(self):
        for record in self:
            if record.state == "cancelled":
                return False
            elif record.state == "sold":
                raise UserError('Sold properties cannot be cancelled.')
            else:
                record.state = "cancelled"
                return True

    def action_sell_offer(self):
        for record in self:
            if record.state == "sold":
                return False
            elif record.state == "cancelled":
                raise UserError('Cancelled properties cannot be sold.')
            else:
                record.state = "sold"
                return True
