from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property'
    _order = 'id desc'

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(
        "Available From", copy=False,
        default=lambda self: fields.Datetime.add(fields.Datetime.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Integer(compute="_compute_total_area", readonly=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.uid,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    _check_positive_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price of a property must be strictly positive.",
    )

    _check_positive_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "The selling price of a property must be positive.",
    )

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for property in self:
            if (float_compare(property.selling_price, (0.9 * property.expected_price), 2) == -1):
                raise ValidationError(self.env._("The selling price must be at least 90% of the expected price. You may decrease the expected price if you want to accept this offer."))

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold_property(self):
        for property in self:
            if property.state == "cancelled":
                raise UserError(self.env._("Cancelled properties cannot be sold"))
            property.state = "sold"
        return True

    def action_cancel_property(self):
        for property in self:
            if property.state == "sold":
                raise UserError(self.env._("Sold properties cannot be cancelled"))
            property.state = "cancelled"
        return True

    @api.ondelete(at_uninstall=False)
    def _check_unlink(self):
        for property in self:
            if property.state != "new" and property.state != "cancelled":
                raise UserError(self.env._("Only new and cancelled properties can be deleted!"))

    @api.onchange("offer_ids")
    def _onchange_offer_ids(self):
        for property in self:
            if len(property.offer_ids) == 0:
                property.state = "new"
            elif property.state != "offer_accepted":
                property.state = "offer_received"
