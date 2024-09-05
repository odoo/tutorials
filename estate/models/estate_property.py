from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    availability_date = fields.Date(copy=False)
    expected_price = fields.Float(required=True, default=0.0)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    best_price = fields.Float(compute="_compute_best_price")
    total_area = fields.Float(compute="_compute_total")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer_received'),
        ('offer_accepted', 'Offer_accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
        ('refused', 'Refused')
    ], string='Status', default='new', tracking=True)
    active = fields.Boolean(string='Active', default=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    seller_id = fields.Many2one('res.users', string="Salesperson", ondelete='set null')
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    property_image = fields.Binary(string="Property Image")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10.0
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0.0
            self.garden_orientation = False

    def action_cancel(self):
        if self.state != "sold":
            self.state = "canceled"
        elif self.state == "sold":
            raise UserError("This property can't be canceled as it is sold already")
        return True

    def action_sold(self):
        if self.state != "canceled":
            if self.state == 'offer_accepted':
                self.state = "sold"
            else:
                raise UserError("This property can't be sold as there are no offers")
        elif self.state == "canceled":
            raise UserError("This property can't be sold as it is canceled already")
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) == -1:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    def action_offer_received(self):
        self.state = 'offer_received'

    @api.ondelete(at_uninstall=False)
    def _delete_property(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(
                    "You cannot delete a property unless it is in the 'New' or 'Canceled' state."
                )
