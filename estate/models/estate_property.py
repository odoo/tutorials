from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
    )
    tag_ids = fields.Many2many(
        comodel_name='estate.property.tag',
        string='Tags',
    )
    date_availability = fields.Date(
        string='Available From',
        copy=False,
        default=lambda self: fields.Date.add(
            fields.Date.today(),
            days=90,
        ),
    )
    expected_price = fields.Float(
        string='Expected Price',
        required=True,
    )
    selling_price = fields.Float(
        string='Selling Price',
        readonly=True,
        copy=False,
    )
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Number of Facades')
    garage = fields.Boolean('is Garage')
    garden = fields.Boolean('is Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled")
        ],
        default="new",
        required=True,
        copy=False,
    )
    buyer = fields.Many2one(
        comodel_name='res.partner',
        string='Buyer',
        copy=False,
    )
    salesman = fields.Many2one(
        comodel_name='res.users',
        string='Salesman',
        default=lambda self: self.env.user,
    )
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string='Offers',
    )
    total_area = fields.Integer(
        string="Total area",
        compute="_compute_total_area",
        readonly=True,
    )
    best_price = fields.Float(
        string='Best Offer',
        compute="_compute_best_price",
        readonly=True,
    )

    _check_expected_price = models.Constraint(
        definition='CHECK(expected_price > 0)',
        message='The expected price must be positive',
    )

    _check_selling_price = models.Constraint(
        definition='CHECK(selling_price >= 0)',
        message='The selling price must be positive',
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Cannot set property to sold if it is canceled")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Cannot set property to canceled if it is sold")
            record.state = "canceled"
        return True
