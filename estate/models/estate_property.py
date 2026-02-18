from odoo import api, exceptions, fields, models, tools


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is my first model"

    # Atomic fields
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), month=3))
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
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation of the estate",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
            ],
        help='Status of the estate',
        default='new',
    )

    # Relational fields
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed fields
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    # Constraints
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price should be strictly greater than zero!',
    )

    _check_seling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The seling price should be greater than zero!',
    )

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if tools.float_is_zero(record.selling_price, precision_digits=2) is True:
                continue

            if tools.float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 1:
                error_message = "Selling price can not be lower than 90% of the expected price"
                raise exceptions.ValidationError(error_message)

    # Compute methods
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.garden_area or 0) + (record.living_area or 0)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0) or 0

    # Onchange
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden is True:
            self.garden_orientation = 'north'
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = False

    # Button logic
    def sold_button(self):
        for record in self:
            if record.state == 'cancelled':
                error_message = "This estate property is cancelled. You can not sell it!"
                raise exceptions.UserError(error_message)
            record.state = 'sold'

        return True

    def cancelled_button(self):
        for record in self:
            if record.state == 'sold':
                error_message = "This estate property is sold. You can not cancel it!"
                raise exceptions.UserError(error_message)
            record.state = 'cancelled'

        return True
