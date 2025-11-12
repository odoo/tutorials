from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils, _


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    name = fields.Char('Name', required=True, default='Unknown Property')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        "Date Availability",
        default=lambda self: fields.Date.to_string(fields.Date.context_today(self) + relativedelta(months=3))
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string='Garden Orientation'
    )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
         ('sold', 'Sold'), ('canceled', 'Canceled')],
        string='Status', default='new', required=True, copy=False
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area", readonly=True)
    best_price = fields.Float(compute="_compute_best_price", string="Best Price", readonly=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must strictly be Positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must strictly be positive.'),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices, default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if self.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise UserError("Canceled properties can't be sold")
            return True

    def action_cancel(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise UserError("Sold properties can't be sold")
        return True

    @api.constrains('selling_price')
    def _check_price(self):
        for record in self:
            if not record.selling_price:
                continue

            if float_utils.float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=3) == -1:
                raise ValidationError(_('The selling cannot be lower than 90% of the expected price.'))

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_check(self):
        if any(record.state not in ('new', 'canceled') for record in self):
            raise UserError(_("You cannot delete a property that is not in the 'New' or 'Canceled' state."))
