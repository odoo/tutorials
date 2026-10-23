from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garages = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new',
        copy=False,
        readonly=True
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.uid)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'A property expected price must be strictly positive'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'A property selling price must be positive'
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError("The selling price cannot be lower than 90 percent of the expected price")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _check_state(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError("You can only delete new and canceled properties!")

    def action_cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise UserError("Sold property cannot be canceled!")

    def action_sell(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise UserError("Canceled property cannot be sold!")
