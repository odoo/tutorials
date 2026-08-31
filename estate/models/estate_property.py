from odoo import api, exceptions, fields, models
from odoo.tools import _, float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate properties"

    title = fields.Char(required=True, default="Unknown")
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    description = fields.Text()
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From",
        default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East')],
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.types", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    tags_id = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
    )
    best_price = fields.Integer(
        "Best Price",
        compute="_compute_best_price"
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'The expected price must be greater than zero (0)',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be greater than zero (0)',
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(
                record.offer_ids.mapped("price"),
                default=0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = ""
            self.garden_area = 0

    def action_sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError(_("Cancelled properties cannot be sold"))
            record.state = "sold"
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError(_("Sold properties cannot be cancelled"))
            record.state = "cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_constraint(self):
        for record in self:
            if float_utils.float_compare(
                    record.selling_price, record.expected_price * 0.9, precision_digits=2
            ) < 0:
                raise exceptions.UserError(_(
                    "The selling price cannot be lower than 90% of the expected price."
                ))
