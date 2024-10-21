from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate property"

    _sql_constraints = [
        ('check_posiive_expected_price', 'CHECK(expected_price > 0)', "The expected price must be strictly positive."),
        ('check_positive_selling_price', 'CHECK(selling_price > 0)', "The selling price must be strictly positive."),
    ]
    _order = "id desc"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3),
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('N', "North"), ('S', "South"), ('E', "East"), ('W', "West")],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Canceled"),
        ],
        required=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesman_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', "property_id", string="Offers")
    total_area = fields.Integer(string="Total Area (sqm)", compute='_compute_total_area')
    best_price = fields.Integer(string="Best Offer", compute='_compute_best_price')

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for estate in self:
            estate.best_price = max(estate.offer_ids.mapped('price'), default=False)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'N'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_sold(self):
        self.ensure_one()
        if self.state == 'canceled':
            raise UserError(_("Canceled properties cannot be sold."))
        self.state = 'sold'
        return True

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'sold':
            raise UserError(_("Sold properties cannot be canceled."))
        self.state = 'canceled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for estate in self:
            if (
                not float_is_zero(estate.selling_price, 3)
                and float_compare(estate.selling_price, estate.expected_price * 0.9, 3) == -1
            ):
                raise ValidationError(_("The selling price cannot be lower than 90% of the expected price."))

    @api.ondelete(at_uninstall=False)
    def _unlink_expecpt_new_and_sold_properties(self):
        if any(estate.state in ('new', 'sold') for estate in self):
            raise UserError(_("Can't delete new or sold properties."))
