from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    # Each field becomes a column in PostgreSQL table
    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Direction",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offers")
    total_area = fields.Float(string="Total Area", compute="_compute_total_area", store=True)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    maintenance_ids = fields.One2many("estate.property.maintenance", "property_id")
    total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            if property.offer_ids:
                property.best_price = max(property.offer_ids.mapped('price'))
            else:
                property.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError("Sold property cannot be cancelled")
            if not property.buyer_id:
                raise UserError("Without accept any offer we can't sold it")
            if property.maintenance_ids:
                for maintenance in property.maintenance_ids:
                    if maintenance.status in ('new', 'cancle'):
                        raise UserError("Maintenance cost must be Approved or Done")
            property.state = 'sold'
        return True

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("Cancelled property cannot be sold")
            property.state = 'cancelled'
        return True

    _check_expected_price_positive = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be strictly positive.',
    )

    _check_selling_price_positive = models.Constraint(
        'CHECK(selling_price > 0)',
        'Selling price must be positive.',
    )

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_digits=2):
                continue

            minimum_price = property.expected_price * 0.9

            if float_compare(property.selling_price, minimum_price, precision_digits=2) < 0:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    @api.depends('maintenance_ids.cost')
    def _compute_total_cost(self):
        for maintenance in self:
            maintenance.total_cost = sum(maintenance.maintenance_ids.mapped('cost'))

    @api.ondelete(at_uninstall=False)
    def _check_property_deletion(self):
        for property in self:
            if property.state not in ('new', 'cancelled'):
                raise UserError("You can only delete properties in New or Cancelled state")
