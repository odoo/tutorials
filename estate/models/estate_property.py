from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property estates"

    state = fields.Selection(
        default='New',
        string='Stage',
        selection=[('New', 'New'), ('Offer_Received', 'Offer Received'), ('Offer_Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Canceled', 'Canceled')],
    )
    active = fields.Boolean(default=True)


    property_type = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        default=lambda self: self.env['estate.property.type'].search([], limit=1)
    )
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, 
        default=fields.Date.add(fields.Date.today(), months=3) # default 3 months from now
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('North', 'North'), ('East', 'East'), ('South', 'South'), ('West', 'West')],
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offers_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # computed fields
    total_area = fields.Float(compute="_total_area")
    best_price = fields.Float(compute="_best_price")

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be strictly positive.'),
    ]
    
    @api.constrains('selling_price')
    def _selling_against_expected_check(self):
        for record in self:
            if float_is_zero(record.selling_price, 2):
                continue
            
            # error if (selling price < 90% of expected_price)
            if float_compare(record.selling_price, record.expected_price * 0.9, 2) == -1:
                raise ValidationError(_('Selling price must be at least 90% of expected price'))


    @api.depends("garden_area", "living_area")
    def _total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offers_ids")
    def _best_price(self):
        for record in self:
            if record.offers_ids:
                record.best_price = max(record.offers_ids.mapped('price'))
            else:
                record.best_price = None

    # onchanges
    @api.onchange("garden")
    def _onchange_garden_bool(self):
        for record in self:
            if record.garden == True:
                self.garden_area = 10
                self.garden_orientation = 'North'
            else:
                self.garden_area = None
                self.garden_orientation = None

    # actions
    def action_mark_as_sold(self):
        self.ensure_one()
        if self.state == 'Canceled':
            # _ underscore is for translation
            raise UserError(_('Cancelled properties cannot be sold'))
        self.state = 'Sold'
        return True # have to return somehing from public methods so XML-RPC layer(?) works

    def action_mark_as_cancelled(self):
        self.ensure_one()
        if self.state == 'Sold':
            raise UserError(_('Sold properties cannot be cancelled'))
        self.state = 'Canceled'
        return True # have to return somehing from public methods so XML-RPC layer(?) works