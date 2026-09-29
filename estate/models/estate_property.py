from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms_count = fields.Integer(default=2)
    living_area = fields.Integer()
    facades_count = fields.Integer()
    has_garage = fields.Boolean()
    has_garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], help="Garden Orientation (North, South, East, West)")
    active = fields.Boolean(default=True)
    stage = fields.Selection([("new", "New"), ("offer received", "Offer Received"), ("offer accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
    required=True, default="new", copy=False)
    property_type_id = fields.Many2one("estate.property.type", "Property Type")
    buyer_id = fields.Many2one("res.partner", "Buyer")
    salesperson_id = fields.Many2one("res.users", "SalesPerson")
    property_tags_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", "Offers")
    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_offer")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be strictly positive'
    )

    _check_selling_price = models.Constraint(
        'CHECK (selling_price > 0)',
        'Selling price must be strictly positive'
    )

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("has_garden")
    def _onchange_garden(self):
        for record in self:
            if record.has_garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = None
                record.garden_orientation = None

    def sell_property(self):
        for record in self:
            if record.stage != 'cancelled':
                record.stage = 'sold'
            raise UserError(self.env._("Unable to sell cancelled property"))
        return True

    def cancel_property(self):
        for record in self:
            if record.stage != 'sold':
                record.stage = 'cancelled'
            raise UserError(self.env._("Unable to cancel sold property"))
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_good_pricing(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and float_compare(record.selling_price, record.expected_price * 0.9, 2) < 0:
                raise ValidationError(self.env._("The selling price must be at least 90% of the expected price"))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_stage_new_cancelled(self):
        for record in self:
            if record.stage not in ("new", "cancelled"):
                raise UserError(self.env._("You can only delete properties in stage cancelled or new"))
    
    def set_stage(self, val):
        if val not in ("new", "offer received", "offer accepted", "sold", "cancelled"):
            raise ValidationError(self.env._("Wrong stage value"))
        self.stage = val

