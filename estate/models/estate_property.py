from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties of an estate"
    _order = "id desc"

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Available', copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Orientation Type', selection=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True, copy=False, default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one("res.partner", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        ('check_expected_price_value', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('check_selling_price_value', 'CHECK(selling_price >= 0)',
         'The selling price must be positive.')
    ]

    @api.constrains("selling_price")
    def _check_selling_price_value(self):
        for record in self:
            if record.selling_price > 0.0 and float_utils.float_compare(record.selling_price, record.expected_price * 9.0 / 10.0, precision_rounding=0.1) < 0:
                raise ValidationError("The selling price cannot be lower than 90 percent of the expected price.")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion_based_on_state(self):
        for record in self:
            if record.state != "new" and record.state != "cancelled":
                raise UserError("You can only delete a property that is new or cancelled")

    def action_sell_property(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Canceled property cannot be sold.")
            else:
                record.state = "sold"
        return True

    def action_cancel_sell_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be cancelled.")
            elif record.state == "sold":
                pass
            else:
                record.state = "cancelled"
        return True
