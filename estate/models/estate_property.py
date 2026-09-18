from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties of the estate"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", copy=False)
    best_offer = fields.Float(compute="_compute_best_offer", string="Best Offer", store=True)

    postcode = fields.Char()
    date_availability = fields.Date(copy=False, string="Available From", default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, string="Selling Price", copy=False)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facade = fields.Integer(string="Façade")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area", store=True)

    active = fields.Boolean(default=True)
    locked = fields.Boolean(compute="_compute_locked", string="Locked", store=True)
    state = fields.Selection(
        string="Status",
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        required=True,
        copy=False,
        default="new",
    )

    _positive_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price should be strictly positive.',
    )

    _positive_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price should be strictly positive.',
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and float_compare(record.selling_price, record.expected_price * 0.9, 2) == -1:
                raise ValidationError(_("The selling price must be at least 90% of the expected price !"))

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price", "offer_ids.status")
    def _compute_best_offer(self):
        for record in self:
            valid_offers = record.offer_ids.filtered(lambda offer: offer.status != "refused")
            record.best_offer = max(valid_offers.mapped("price"), default=0)

    @api.depends("state")
    def _compute_locked(self):
        for record in self:
            record.locked = record.state in ("sold", "cancelled")

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _only_if_new_or_cancelled(self):
        for record in self:
            if record.state != 'new' and record.state != 'cancelled':
                raise UserError(_("Can't delete property that is not new or cancelled !"))

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("A cancelled property cannot be sold !"))
            if not record.offer_ids.filtered(lambda offer: offer.status == "accepted"):
                raise UserError(_("A property with no accepted offer can't be sold !"))
            record.state = "sold"
        return True

    def action_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("A sold property cannot be cancelled !"))
            record.state = "cancelled"
        return True

    def _update_state_from_offers(self):
        for record in self:
            if record.offer_ids.filtered(lambda offer: offer.status == "accepted"):
                record.state = "offer_accepted"
            elif any(not offer.status for offer in record.offer_ids):
                record.state = "offer_received"
            else:
                record.state = "new"
