from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    expected_price = fields.Float(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    active = fields.Boolean(default=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        help="The direction the garden faces."
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
)

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
)
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
)
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
)
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
        copy=True
)
    total_area = fields.Integer(
        compute="_compute_total_area",
        string="Total Area (sqm)",
)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = (
                record.living_area +
                record.garden_area
)
    best_price = fields.Float(
        compute="_compute_best_price",
        string="Best Offer",
)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(
                    record.offer_ids.mapped("price")
                )
            else:
                record.best_price = 0.0

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
            if record.state == 'canceled':
                raise UserError(
                "Cancelled property cannot be sold!"
            )
            record.state = 'sold'
            return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(
                "Sold property cannot be cancelled!"
            )
            record.state = 'canceled'
        return True
