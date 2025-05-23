from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, api
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)

    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()

    garden_orientation = fields.Selection([('North', 'north'), ('South', 'south'), ('West', 'west'), ('East', 'east')])
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')], required=True, copy=False, default='new')
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one('estate.property.type')
    buyer = fields.Many2one('res.partner', readonly=True)
    seller = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tags = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    total_area = fields.Float(compute="_compute_total_area")
    garden_area = fields.Integer()
    living_area = fields.Integer()

    best_offer = fields.Integer(compute='_compute_best_offer')

    _order = 'id desc'

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be strictly positive.'),
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, (record.expected_price/ 10)* 9, 4) == -1:
                raise ValidationError("The selling price must be at least 90% of the expected price.")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _compute_best_offer(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            if len(prices) > 0:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 1000
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sold(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = "sold"
            else:
                raise UserError("Cancelled properties cannot be sold.")
        return True

    def cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = "cancelled"
            else:
                raise UserError("Sold properties cannot be cancelled.")
        return True

    @api.onchange("offer_ids")
    def _onchange_offer(self):
        if self.offer_ids:
            self.state = 'offer_received'
        else:
            self.state = 'new'

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        for record in self:
            if record.state != 'new' and record.state != 'cancelled':
                raise UserError("Only new and cancelled properties can be deleted.")

