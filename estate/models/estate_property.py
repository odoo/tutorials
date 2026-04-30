from odoo import exceptions, api, fields, models
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _name = "estate.property"
    _description = "Properties"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
            required=True,
            copy=False,
            default='new',
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    sales_person_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_living_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_living_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.mapped("offer_ids.price"), default=0.0)

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'A property expected price must be strictly positive',
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'A property selling price must be positive',
    )

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_area = 10
                property.garden_orientation = 'north'
            else:
                property.garden_area = 0
                property.garden_orientation = None

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise exceptions.UserError("Cannot cancel a sold peoperty")
            else:
                property.write({
                    'state': 'cancelled',
                })
        return True

    def action_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise exceptions.UserError("Cannot sell a cancelled peoperty")
            else:
                property.write({
                    'state': 'sold',
                })
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            if property.state == 'offer_accepted':
                if float_compare(property.selling_price, property.expected_price * (90 / 100), precision_rounding=0.01) < 0:
                    raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price.")
