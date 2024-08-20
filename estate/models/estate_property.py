from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This model stores estate properties information and the current state of the sales process"
    _order = "id desc"
    _sql_constraints = [
        ('expected_price_check', 'CHECK (expected_price > 0)', 'the expected price must be strictly positive'),
        ('selling_price_check', 'CHECK (selling_price >= 0)', 'the selling price must be positive')
    ]

    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    property_tag_ids = fields.Many2many("estate.property.tag")

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)
    postcode = fields.Char(string="Postcode")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden", default=False)
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    garden_area = fields.Integer(string="Garden Area (sqm)")
    living_area = fields.Integer(string="Living Area (sqm)")
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    expected_price = fields.Float(string="Expected Price", required=True)
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    date_availability = fields.Date(string="Available From", default=fields.Datetime.add(fields.Datetime.today(), months=3), copy=False)
    state = fields.Selection(string="", required=True, default="new", copy=False, selection=[
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ])

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for estate in self:
            estate.best_price = max(estate.offer_ids.mapped('price') + [0])

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for estate in self:
            if (estate.state == 'offer_accepted') and (tools.float_utils.float_compare(estate.expected_price * 0.9, self.selling_price, precision_digits=2) == 1):
                raise UserError(_("The selling price is too low (<90" + "%" + " of the expected price)"))

    @api.onchange("garden")
    def _onchange_garden_info(self):
        for estate in self:
            if estate.garden:
                estate.garden_area = 10
                estate.garden_orientation = 'north'
            else:
                estate.garden_area = 0
                estate.garden_orientation = ''

    @api.ondelete(at_uninstall=False)
    def _unlink_except_pending(self):
        for estate in self:
            if estate.state in ('offer_received', 'offer_accepted', 'sold'):
                raise UserError(_("Cannot delete a property if not new or canceled"))

    def estate_property_button_sold(self):
        for estate in self:
            if estate.state == 'canceled':
                raise UserError(_("A canceled property cannot be set as sold"))
            else:
                estate.state = 'sold'

    def estate_property_button_cancel(self):
        for estate in self:
            if estate.state == 'sold':
                raise UserError(_("A sold property cannot be canceled"))
            else:
                estate.state = 'canceled'
