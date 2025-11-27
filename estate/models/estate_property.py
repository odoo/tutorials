from odoo import api, fields, models, _
from odoo.tools import float_compare
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property model"
    _order = "id desc"

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price of the property must be strictly positive.',
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price of the property must be strictly positive.',
    )

    name = fields.Char("Title", required=True, default="Unknown")
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    expected_price = fields.Float("Expected Price", required=True)
    date_availability = fields.Date(
        "Available From",
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False,
    )
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[("north", "N"), ("south", "S"), ("east", "E"), ("west", "W")],
        help="Orientation of the garden",
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )

    property_type_id = fields.Many2one(
        'estate.property.type', string='Property Type', ondelete='restrict'
    )

    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesman',
        ondelete='restrict',
        default=lambda self: self.env.user.partner_id,
    )

    buyer_id = fields.Many2one(
        'res.partner', string='Buyer', ondelete='restrict', copy=False, readonly=True,
    )

    property_tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    color = fields.Integer('Color Index', default=7)

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area, self.garden_orientation = 10, "north"
        else:
            self.garden_area, self.garden_orientation = 0, None

    def action_mark_as_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("Canceled properties cannot be sold."))
            record.state = "sold"
            record.active = False
        return True

    def action_mark_as_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Sold properties cannot be cancelled."))
            record.state = "cancelled"
            record.active = False
        return True

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            for offer in record.offer_ids:
                if offer.status == "yes" and float_compare(offer.price, 0.9 * record.expected_price, 2) < 0:
                    raise ValidationError("There is an accepted offer for an amount less than 90 percent of the new selling price, action required!")

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        if self.state not in ('new', 'cancelled'):
            raise ValidationError("Only new and canceled properties can be deleted.")
