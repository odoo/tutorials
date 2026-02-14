from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.tools.sql import SQL


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'estate property details'
    _order = 'id desc'
    _inherit = 'mail.thread'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today() + timedelta(days=90)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('west', "West"),
            ('east', "East"),
            ('south', "South"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one(
        'estate.property.type', string="Property Type")
    user_id = fields.Many2one(
        'res.users', string="Salesperson", default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer", readonly=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id')
    total_area = fields.Integer(
        compute='_compute_total_area', string="Total Area(sqm)")
    best_price = fields.Float(
        compute='_compute_best_price', search='_search_best_price')
    property_maintainance_ids = fields.One2many(
        'estate.property.maintenance', 'property_id')
    total_maintenance_cost = fields.Float(
        compute='_compute_total_maintenance_cost')
    investor = fields.Many2one('estate.investor')
    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        "The Expected price cannot be negative or zero."
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        "The Selling price cannot be negative."
    )

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = None
        # best_price = dict(self.env['estate.property.offer']._read_group(domain=[
        #                   ('property_id', 'in', self.ids)], aggregates=['price:max'], groupby=['property_id']))
        # for record in self:
        #     record.best_price = best_price.get(record, 0.0)

    def _search_best_price(self, operator, value):
        if operator in ('in', 'not in'):
            value = tuple(value)
        sql = SQL("""
        SELECT property_id FROM estate_property_offer GROUP BY property_id HAVING MAX(price) %s %s
        """, SQL(operator), value)
        f = self.env.execute_query(sql)
        return [('id', 'in', f)]

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains('selling_price', 'expected_price')
    def _constraint_selling_price(self):
        if float_is_zero(self.selling_price, precision_rounding=0.01):
            return
        elif float_compare(self.selling_price, self.expected_price * 0.9, precision_rounding=0.01) < 0:
            raise ValidationError(_(
                "Selling price cannot be lower than 90% of the expected price."))

    def action_property_sold(self):
        if self.state != 'offer_accepted':
            raise UserError(_("Atleast one offer should be accepted."))
        for record in self.property_maintainance_ids:
            if record.status != 'done':
                raise UserError(_("Maintenance Request are still pending."))
        self.state = 'sold'
        self.active = False

        template = self.env.ref(
            'estate.mail_template_property', raise_if_not_found=False)
        ctx = {
            'default_model': 'estate.property',
            'default_res_ids': self.ids,
            'default_composition_mode': 'comment',
            'default_template_id': template.id,
        }
        action = {
            'name': _('Send'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
        return action

    def action_property_cancel(self):
        self.state = 'cancelled'

    def action_accept_best_offer(self):
        data = self.env['estate.property.offer'].search(
            domain=[('property_id', 'in', self.ids), ('price', '=', self.best_price)], limit=1)
        data.action_accepted()

    @api.depends('property_maintainance_ids.cost', 'property_maintainance_ids.property_id')
    def _compute_total_maintenance_cost(self):
        for record in self:
            record.total_maintenance_cost = sum(
                record.property_maintainance_ids.mapped('cost')) or 0
        # maintenace_cost = dict(self.env['estate.property.maintenance']._read_group(domain=[(
        #     'property_id', 'in', self.ids)], aggregates=['cost:sum'], groupby=['property_id']))
        # for record in self:
        #     record.total_maintenance_cost = maintenace_cost.get(record, 0.0)

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        if self.state not in ['new', 'cancelled']:
            raise UserError(
                _("Only new and cancelled property can be deleted."))

    def action_print_doc(self):
        return self.env.ref("estate.estate_property_report").report_action(self)
