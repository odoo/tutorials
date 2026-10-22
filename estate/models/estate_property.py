from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

default_availability_date = (fields.Datetime.add(fields.Datetime.today(), days=90))


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    property_type_id = fields.Many2one("estate.property.type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: default_availability_date)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West"),
    ])
    active = fields.Boolean(default=True)
    state = fields.Selection(required=True, copy=False, default="new", selection=[
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled"),
    ])
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    accepted_offer_id = fields.Many2one('estate.property.offer', copy=False, readonly=True)

    _check_expected_price_positive = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be greater than 0.'
    )
    _check_selling_price_positive = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be greater than 0.'
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_min(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_price = record.expected_price * 0.90
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError('The selling price cannot be lower than 90%% of the expected price.')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else None
        self.garden_orientation = 'north' if self.garden else None

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")

            if not bool(record.accepted_offer_id):
                raise UserError("A offer must be accepted before a property can be marked as sold")

            record.state = "sold"

        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled")

            record.state = "cancelled"

        return True

    def action_revert_draft(self):
        for record in self:
            if bool(record.accepted_offer_id):
                record.state = 'offer_accepted'
            elif record.offer_ids:
                record.state = 'offer_received'
            else:
                record.state = 'new'

        return True
