from odoo import api, fields, models
from odoo.tools import float_compare
from odoo.tools.date_utils import add
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "description"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Garden orientation is used to describe orientation of garden",
    )

    tags_ids = fields.Many2many("estate.property.tag")

    partner_id = fields.Many2one("res.partner", string="Partner")
    property_type_id = fields.Many2one("estate.property.type")

    salesman = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer = fields.Many2one("res.partner", string="Buyer")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Recieved"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Canceled"),
        ],
        copy=False,
        default='new',
        required=True,
    )

    total_area = fields.Float(compute='_compute_total', string="Total area (sqm)")
    best_price = fields.Float(compute='_compute_best_price', string="Best offer")

    _sql_constraints = [
        (
            'check_expected_price',
            'CHECK(expected_price > 0)',
            'A property expected price must be strictly positive.',
        ),
        (
            'check_selling_price',
            'CHECK(selling_price > 0)',
            'A property selling price must be positive.',
        ),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = 0
            for offer in record.offer_ids:
                record.best_price = max(record.best_price, offer.price)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")

            record.state = "sold"

        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled")

            record.state = "cancelled"

        return True

    @api.constrains(
        'selling_price',
        'expected_price',
    )
    def _check_selling_price(self):
        for record in self:
            for offer in record.offer_ids:
                if (
                    float_compare(offer.price, 0.9 * record.expected_price, precision_digits=5)
                    == -1
                    and offer.status == 'accepted'
                ):
                    raise ValidationError(
                        "An offer lower than 90% of expected price cannot be accepted."
                    )
