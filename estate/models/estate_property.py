from odoo import api, exceptions, fields, models
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Information about the properties"
    _check_expected_price = models.Constraint('CHECK(expected_price > 0.0)')
    _check_selling_price = models.Constraint('CHECK(selling_price >= 0.0)')
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[("north", "North"), ("east", "East"), ("south", "South"), ("west", "West")])
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        string="Status",
        default="new",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_offer")

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = record.best_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_is_valid(self):
        if not float_utils.float_is_zero(self.selling_price, precision_digits=2) and float_utils.float_compare(
            self.selling_price, 0.9 * self.expected_price, precision_digits=2) < 0:
            raise exceptions.ValidationError(self.env._("The selling price cannot be lower than 90% of the expected price."))

    def action_mark_as_sold(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise exceptions.UserError('Cannot set a property to "Sold" after the listing has been cancelled.')
        elif self.state == "sold":
            raise exceptions.UserError('This property has already been sold.')
        else:
            self.state = "sold"
        return True

    def action_cancel_listing(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise exceptions.UserError(self.env._('This property listing has already been cancelled.'))
        else:
            self.state = "cancelled"
        return True

    @api.ondelete(at_uninstall=False)
    def _prevent_unlink_by_status(self):
        for record in self:
            if record.state not in {"new", "cancelled"}:
                raise exceptions.UserError(self.env._("You cannot delete this property."))
