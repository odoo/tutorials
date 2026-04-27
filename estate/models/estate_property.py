from odoo import api, fields, models, exceptions, tools


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    name = fields.Char('Property Name', required=True)
    description = fields.Text()
    property_type_id = fields.Many2one('estate.property.type')
    buyer_id = fields.Many2one('res.partner', copy=False)
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.uid)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    postcode = fields.Char()
    date_availability = fields.Date('Availability Date', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float('Best Offer', compute="_compute_best_price")
    selling_price = fields.Float(compute="_compute_selling_price", readonly=True, copy=False)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        required=True,
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for line in self:
            line.best_price = max(line.mapped('offer_ids.price'), default=0)

    @api.depends('offer_ids.status', 'offer_ids.price')
    def _compute_selling_price(self):
        for line in self:
            accepted_offer = line.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offer:
                line.selling_price = accepted_offer[0].price
                line.buyer_id = accepted_offer[0].partner_id
            else:
                line.selling_price = 0

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("You cannot cancel a sold property.")
            else:
                record.state = 'cancelled'
        return True

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("You cannot mark a cancelled property as sold.")
            else:
                record.state = 'sold'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if tools.float_is_zero(record.selling_price, precision_digits=2):
                continue

            if tools.float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise exceptions.ValidationError("The selling price cannot be less than 90% of the expected price.")

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'
