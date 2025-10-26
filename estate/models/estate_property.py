from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class PropertyModel(models.Model):
    _name = "estate.property"
    _description = "Estate Property model"
    _order = "id desc"

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    best_offer = fields.Float(compute="_compute_highest_price")
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    total_living_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        string="Status",
        required=True,
        copy=False,
        default="new"
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    _check_positive_expected_price = models.Constraint(
        "CHECK(expected_price >= 0)",
        "The expected price must be positive."
    )
    _check_positive_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_living_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_highest_price(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price")) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = self.env["ir.config_parameter"].get_param("estate.default_garden_area")
            self.garden_orientation = self.env["ir.config_parameter"].get_param("estate.default_garden_orientation")
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and float_compare(record.selling_price, record.expected_price * .9, 0) == -1:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        if any(record.state not in ('new', 'cancelled') for record in self):
            raise UserError(_("Only 'New' and 'Cancelled' properties can be deleted."))

    def action_mark_as_sold(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise UserError(_("A cancelled property cannot be set as sold."))
        if not any(offer.status == "accepted" for offer in self.offer_ids):
            raise UserError(_("A property must have an accepted offer to be marked as sold."))
        self.state = "sold"
        return True

    def action_mark_as_cancelled(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError(_("A sold property cannot be set as cancelled."))
        self.state = "cancelled"
        return True
