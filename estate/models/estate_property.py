from dateutil.relativedelta import relativedelta
from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = 'Listing for the properties'
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", required=True, tracking=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='PostCode', index=True)
    date_availability=fields.Date(
        string='Available Date',
        default=lambda self: date.today()+relativedelta(months=3),
        copy=False
    )
    expected_price = fields.Float(string='Expected Price', required=True, tracking=True)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(
        string='Facades',
        help="a facade refers to the front or exterior appearance of a building, usually facing the street."
    )
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area(sqm)')
    garden_orientation = fields.Selection(
        string="Gardern Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East')
        ])
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readonly=True)
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store="True", tracking=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    total_area = fields.Integer(string="Total Area(sqm)", compute="_compute_total_area", store="True")
    property_image = fields.Binary("Image", attachment=True)

#---------------get best price-----------------------------#
    @api.depends('property_offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.property_offer_ids:
                record.best_price = max(record.property_offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

#--------------compute total area---------------------------#
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

#---------------on click sold button---------------------------#
    def action_sold_button(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_('Cancelled property cannot be sold.'))
            if record.state != 'offer_accepted':
                raise UserError(_('Not an any offer has Accepted.'))
            else:
                record.state = 'sold'
        return True

#--------------on click cancel button--------------------------#
    def action_cancel_button(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('Property Is already Sold'))
            else:
                record.state = 'cancelled'
        return True

#--------------on click multiple offer button-----------------#
    def action_estate_property_multiple_offer(self):
        return {
            "name" : 'Add Multiple Offers',
            'type' : 'ir.actions.act_window',
            "res_model" : 'estate.property.multiple.offer',
            "view_mode" : 'form',
            "target" : 'new'
        }

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be greater than zero!'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be greater than zero!')
    ]

#---------------check selling price >= 90% of expected price--------------------#
    @api.constrains('selling_price', 'expected_price')
    def _check_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=6):
                return

            min_selling_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_selling_price, precision_digits=6) < 0:
                raise ValidationError(_("Selling price cannot be less than 90% of the expected price!"))

#---------------only new and cancel property can delete------------------------#
    @api.ondelete(at_uninstall=False)
    def _unlink_stete_not_new_or_cancel(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(_('Only new or cancelled properties can be deleted!'))
