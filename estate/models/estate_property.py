from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'  # . will be shown as _ in actual database 
    _description = 'listing for the properties'
    _order = 'id desc'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Post Code", index=True)

    date_availability = fields.Date(
        string="Date Availability",
        default=lambda self:date.today()+relativedelta(months=3),
        copy=False
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")

    facades = fields.Integer(
        string="Facades",
        help="A facade in real estate is the exterior wall of a building, usually the front face."
    )

    garage = fields.Boolean(string="Garage?")
    garden = fields.Boolean(string="Garden?")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
        ])

    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='Status',
        selection=[
            ('new','New'),
            ('offer_received','Offer Received'),
            ('offer_accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson = fields.Many2one('res.users', string='Salesman', default=lambda self:self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', string="Offers")
    total_area = fields.Float(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Integer(string='Best Offer', compute='_compute_best_price')
    company_id = fields.Many2one('res.company', string="Company", default = lambda self: self.env.company, required = True)
    image = fields.Binary("Image",attachment = True)

    _sql_constraints = [
        ('expected_price_check', 'CHECK( expected_price >= 0 )', 'A property expected price must be strictly positive'),
        ('selling_price_check', 'CHECK( selling_price >= 0 )', 'A property selling price must be positive')
    ]


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            best_prices = record.offer_ids.mapped('price')
            record.best_price = max(best_prices) if best_prices else 0

    @api.constrains('selling_price', 'expected_price')
    def _validate_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=3):
                return
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=3) < 0:
                raise ValidationError("the selling price cannot be lower than 90 percentage of the expected price")

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold_btn(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            else:
                raise UserError(_("Property which is canceled can't be sold"))
        return True

    def action_cancel_btn(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            else:
                raise UserError(_("Property which is sold can't be cancelled"))
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_not_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new','cancelled']:
                raise UserError(_("You can only delete a property if its state is 'New' or 'Cancelled'."))

    def action_add_offers(self):
        return {
            'name': 'Add Offers',
            'type': 'ir.actions.act_window',
            'res_model': 'estate.add.offers.wizard',
            'view_mode': 'form',
            'target': 'new'
        }
