from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Test Model"
    _order = "id desc"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', default=fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default='2')
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], copy=False, default='new', required=True, readonly=True)
    active = fields.Boolean(string='Active', default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user or False)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_id = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers list")
    total_area = fields.Float(string="Total area", compute="_compute_total_area")
    best_offer = fields.Float(string="Best offer", compute="_compute_best_offer")
    configSold = fields.Boolean(string='Sold Config', compute='_compute_config_sold')

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive.'),
        ('strictly_positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly postive.'),
    ]

    @api.depends('state')
    def _compute_config_sold(self):
        sold_setting = self.env['ir.config_parameter'].sudo().get_param('estate.sold')
        for record in self:
            record.configSold = sold_setting == 'True'

    @api.constrains('expected_price', 'selling_price')
    def check_quantity(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9 and not float_is_zero(record.selling_price, 2):
                raise ValidationError("The selling price must be least 90% of the expected price! You must reduce the expected price if you want to accept this offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(offer_id.price for offer_id in record.offer_ids)
                if not record.state in ['accepted', 'sold', 'canceled']:
                    record.state = 'received'
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_cancel_property(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise UserError("Sold properties can't be canceled")
        return True

    def action_sold_property(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise UserError("Canceled properties can't be sold")
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for record in self:
            domain = ['&', ('state', '!=', 'new'), ('state', '!=', 'canceled')]
            properties = self.env['estate.property'].search(domain)
            if record in properties:
                raise ValidationError("Only New and Canceled Properties can be Deleted.")
