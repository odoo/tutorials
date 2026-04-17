from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate system"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected Price must be strictly positive'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling Price must be positive'
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_price = record.expected_price * 0.90
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    "The selling price can't be lower than 90%% of expected price"
                )

    def _get_default_date_calculation(self):
        return fields.Date.today() + relativedelta(months=3)

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date(string="Available From", copy=False, default=_get_default_date_calculation)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)", help="Living area in square meters")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean(string="Garden", help="Has garden")
    garden_area = fields.Integer(string="Garden Area (sqm)", help="Garden area in square meters")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True, help="Uncheck to archive this property")
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], required=True, copy=False, default='new', tracking=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", ondelete='cascade')
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    seller_id = fields.Many2one('res.users', string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', 'estate_property_tag_rel', 'property_id', 'tag_id', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Float(compute='_compute_total_area', store=True)
    best_price = fields.Float(compute='_compute_best_price', readonly=True, store=True)

    def action_sold(self):
        self.ensure_one()
        if self.state == 'cancelled':
            raise UserError("Cancelled properties cannot be sold.")
        self.state = 'sold'

        ctx = {
            'default_model': 'estate.property',
            'default_res_ids': self.ids,
            'default_partner_ids': self.buyer_id.ids,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'default_subject': f"Property Confirmed: {self.name}",
            'default_body': f"<p>Hello,<br/>The property <b>{self.name}</b> has been sold for <b>${self.selling_price}</b>.</p>",
        }

        return {
            'name': 'Send Email',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': ctx,
        }

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            record.state = 'cancelled'
        return True

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'

    @api.ondelete(at_uninstall=False)
    def _ondelete_check_state(self):
        for records in self:
            if records.state not in ('new', 'cancelled'):
                raise UserError(f"The property state is in {records.state}, you can't delete this property")
