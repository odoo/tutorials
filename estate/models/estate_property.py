from odoo import api, exceptions, fields, models
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = "id desc"

    name = fields.Char(required=True)
    active = fields.Boolean('Active', default=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today().replace(month=(fields.Date.today().month + 3) % 12))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Float(compute="_compute_total_area")
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('south', 'South'), ('north', 'North'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        selection=[('new_property', "New"), ('offer_received', 'Offer received'),
                   ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new_property'
    )
    best_price = fields.Float(compute="_compute_best_price")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tags_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    _expected_price_check = models.Constraint('CHECK(expected_price > 0)', 'The expected price must be strictly positive')
    _selling_price_check = models.Constraint('CHECK(selling_price >= 0)', 'The selling price must be positive')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if (record.garden):
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = None
                record.garden_orientation = None

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if (float_compare(record.selling_price, record.expected_price * 0.9, 2) == -1):
                raise exceptions.ValidationError("The selling price must be at least 90% of the expected price")

    def action_cancel(self):
        for record in self:
            if (record.state == 'sold'):
                raise exceptions.UserError("Sold property cannot be cancelled")
            record.state = 'cancelled'
        return True

    def action_sold(self):
        for record in self:
            if (record.state == 'cancelled'):
                raise exceptions.UserError("Cancelled property cannot be sold")
            record.state = 'sold'
        return True
