from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate module"
    _order = "id desc"

    
    name = fields.Char(required=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=fields.Date.add(fields.Date.today(),months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Orientation',
        selection = [
            ('north', 'North'), 
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
    )

    active = fields.Boolean(default=True)

    state = fields.Selection(
        string = 'State',
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'), 
            ('offer_accepted', 'Offer Accepted'), 
            ('sold', 'Sold'), 
            ('canceled', 'Canceled'),
        ],
        required = True,
        copy = False,
        default = 'new'
    )

    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price should be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be positive')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.onchange("offer_ids")
    def _onchange_offer_ids(self):
        if len(self.offer_ids) == 0:
            self.state = "new"
        else:
            self.state = "offer_received"

    def sold_action(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold.")
            else:
                record.state = "sold"
        return True

    def cancel_action(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            else:
                record.state = "canceled"
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_utils.float_is_zero(record.selling_price, precision_digits=5) and float_utils.float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=5) < 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price")
