from odoo import api, models, fields, exceptions, tools


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _sql_constraints = [
        ("positive_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("positive_selling_price", "CHECK(selling_price >= 0)", "The selling price must be positive"),
    ]
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    total_area = fields.Float(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        default='new',
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    def action_mark_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Sold properties cannot be canceled")
            record.state = 'canceled'
        return True

    def action_mark_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError("Canceled properties cannot be sold")
            record.state = 'sold'
        return True

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price_close_to_expected(self):
        for record in self:
            if not (
                tools.float_utils.float_is_zero(record.selling_price, precision_digits=2) or
                tools.float_utils.float_compare(0.9 * record.expected_price, record.selling_price, precision_digits=2) <= 0
            ):
                raise exceptions.ValidationError("The selling price must be at least 90% of the expected price. Lower the expected price, or find a better offer")
