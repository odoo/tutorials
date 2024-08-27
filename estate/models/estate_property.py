from odoo import models, fields, api, _
from datetime import date
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Estate property"
    _order = 'id desc'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability', copy=False, default=(
        date.today() + relativedelta(months=3)))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area ')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[
                                              ('north', 'North'),
                                              ('south', "South"),
                                              ('east', 'East'),
                                              ('west', 'West'),
                                          ]
                                          )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(string='Status',
                             selection=[
                                 ('new', 'New'),
                                 ('offer received', 'Offer Received'),
                                 ('offer accepted', 'Offer Accepted'),
                                 ('sold', 'Sold'),
                                 ('cancelled', 'Cancelled')
                             ], copy=False, default='new'
                             )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", string="Property Type")
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one(
        comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag", string="Tages")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(string="Total area", compute="_compute_values")
    best_price = fields.Float(string="Best offer", compute="_compute_values")

    # sql constraints
    _sql_constraints = [
        ('check_price', 'CHECK(expected_price > 0)',
         'The Expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'The selling price must be positve')
    ]

    # python constrains
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError(
                    _("Selling price must be greater than 90% of expected price"))

    @api.depends("garden_area", "living_area", "offer_ids.price")
    def _compute_values(self):
        for record in self:
            # for calculating total_area
            record.total_area = record.garden_area + record.living_area

            # for calculating best_price
            record.best_price = max(record.offer_ids.mapped(
                "price")) if record.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold(self):
        if self.state == 'cancelled':
            raise UserError(_("You cannot sold the cancelled property"))
        else:
            self.state = 'sold'

    def action_cancel_property(self):
        if self.state == 'sold':
            raise UserError(_("You cannot cancel the sold property"))
        else:
            self.state = 'cancelled'

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(
                    "You cannot delete a property unless its state is 'New' or 'Cancelled'.")

    def action_add_offer(self):
        properties = self.browse(self.env.context.get("active_ids"))
        unavail_properties = properties.filtered_domain([('state', 'not in', ['new', 'offer received'])])

        if unavail_properties:
            raise UserError(
                "Some properties are not available ! please select available properties only..")

        else:
            return self.env['ir.actions.act_window']._for_xml_id('estate.action_add_offer_wizard')
