from odoo import api, fields, models
from odoo.tools import date_utils
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

def date_in_3_months(*args):
    return date_utils.add(fields.Date.today(), months=3)

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "App to handle your real estate."
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive.'),
         ('check_selling_price', 'CHECK(selling_price >= 0)',
         'A property selling price must be positive.')
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", default=date_in_3_months, copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')],
        default='new',
        copy=False
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) == 0:
                record.best_price = False
                continue
            record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = "south"
        else:
            self.garden_area = False
            self.garden_orientation = False

    def action_set_sold_property(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold.")
            record.state = "sold"
        return True

    def action_set_canceled_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            record.state = "canceled"
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_date_end(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 0.9, 2) < 0 and not float_is_zero(record.selling_price, 2):
                raise ValidationError('The selling price cannot be lower than 90% of the expected price.')
