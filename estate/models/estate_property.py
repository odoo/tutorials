from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "ch3 exercise tutorial"
    _order = "id desc"

    name = fields.Char(required=True)
    # active = fields.Boolean(default=False)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new'
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda _: fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default="2")
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    sales_person = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The Expected price of an estate should be positive.')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0
            if prices and record.state in [None, 'new']:
                record.state = 'offer_received'

    @api.onchange("garden")
    def _onchange_partner_id(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = None
                record.garden_orientation = None

    def action_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")
            else:
                record.state = 'sold'
        return True

    def action_property_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            else:
                record.state = 'cancelled'
        return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price is not None and float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=9) == -1:
                raise ValidationError("The selling price cannot be less than 90% of the expected price")
