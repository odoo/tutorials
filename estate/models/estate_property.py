from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "manage properties"
    _order = "id desc"

    name = fields.Char(string="Name", required=True, default="Unknown")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="PostCode")
    date_availability = fields.Date(string="Availability", copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(string="Excepted price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orentation = fields.Selection(string="Garden orientation", selection=[('north', 'North'), ('south', 'South'), ('ouest', 'West'), ('east', 'East')])
    active = fields.Boolean(default=True)
    states = fields.Selection(string="State", default='new', selection=[('new', 'New'), ('offer_received', 'Offre Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')])

    tags_ids = fields.Many2many("estate_property_tags", string="Tags")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    estate_property_type = fields.Many2one("estate_property_type", string="Property Type")
    offer_ids = fields.One2many(comodel_name="estate_property_offer", inverse_name="property_id", string="Offers")

    total_area = fields.Float(compute="_compute_area", string="Total area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _sql_constraints = [
        ('check_price_positive', 'CHECK(expected_price >= 0)', 'The price should be higher than 0'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price should be higher than 0'),
        ('check_unique_name', 'UNIQUE(name)', 'The name of the property should be unique'),
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink_if_states_match(self):
        for record in self:
            if record.states not in ['new', 'canceled']:
                raise UserError("You can't delete active properties")

    @api.depends("garden_area", "living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange("garden")
    def _update_garden_values(self):
        if self.garden is True:
            self.garden_area = 20
            self.garden_orentation = 'north'
        else:
            self.garden_area = 0
            self.garden_orentation = ''

    def mark_as_sold(self):
        for record in self:
            if record.states == "canceled":
                raise UserError("You can't set a canceled property to sold")
            else:
                record.states = "sold"

    def mark_as_canceled(self):
        for record in self:
            if record.states == "sold":
                raise UserError("You can't cancel a sold property")
            else:
                record.states = "canceled"

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.expected_price != 0:
                min_selling_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_selling_price, 2) == -1:
                    raise ValidationError("Selling price shoudn't be lower than 90% of expected price")
