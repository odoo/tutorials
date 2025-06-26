from odoo import api, fields, models, _
from odoo.tools import date_utils, float_utils
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price of an property should be positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price of an property should be positive.')
    ]
    _order = "id desc"


    name = fields.Char(string='Estate Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_available = fields.Date(string='Available From Date', copy=False, default=date_utils.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Has a Garage')
    garden = fields.Boolean(string='Has a Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[
        ('north', "North"),
        ('south', "South"),
        ('east', "East"),
        ('west', "West")
    ])
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(string='State', required=True, copy=False, default='new', selection=[
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled")
    ])

    type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", 'property_id', string="Offers")

    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = None
            self.garden_area = 0

    @api.onchange("offer_ids")
    def _onchange_offers(self):
        if len(self.offer_ids) != 0:
            self.state = 'offer_received'
        else:
            self.state = 'new'

    @api.constrains("expected_price", "selling_price")
    def check_selling_price(self):
        # This function check that the selling price is not lower than 90% of the expected price
        for record in self:
            if (not float_utils.float_is_zero(record.selling_price, precision_digits=2)
                    and float_utils.float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0):
                raise ValidationError("Selling price can't be lower than 90% of expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_properties(self):
        if any(record.state not in ['new', 'cancelled'] for record in self):
            raise UserError("Can't delete ongoing property selling.")

    def action_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties can't be sold.")
            else:
                record.state = "sold"

        return True

    def action_property_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties can't be cancelled.")
            else:
                record.state = "cancelled"

        return True
