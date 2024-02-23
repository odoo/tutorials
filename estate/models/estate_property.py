from odoo import models, fields, api, exceptions
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help="Orientation is used to separate different garden orientations")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        default='new',
        required=True,
        copy=False,
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ]
    )
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    salesperson_id = fields.Many2one(
        'res.users', string='Salesman', default=lambda self: self.env.user)

    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")

    estate_property_tag_ids = fields.Many2many(
        "estate.property.tag", string="Tags")

    _sql_constraints = [
        ('check_positive_expected_price', 'CHECK(expected_price > 0)',
         'The expected price should be positive.'),
        ('check_positive_selling_price', 'CHECK(selling_price > 0)',
         'The selling price should be positive.'),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped(
                "price")) if len(record.offer_ids) > 0 else None

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_set_cancel_state(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError(
                    message="A sold property can not be canceled")
            record.state = 'canceled'
        return True

    def action_set_sold_state(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError(
                    message="A canceled property can not be sold")
            record.state = 'sold'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price:
                if float_utils.float_compare(record.selling_price, 0.9*record.expected_price, 2) < 0:
                    raise exceptions.ValidationError(
                        message="The selling price must be greater that 90% of the expected price!")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_sold_or_canceled_property(self):
        for record in self:
            if not (record.state == 'new' or record.state == 'canceled'):
                raise exceptions.UserError(
                    f"You can not delete a property in {record.state} state.")
