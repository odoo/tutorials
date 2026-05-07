from odoo import _, fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):

    _name = 'estate.property'
    _description = "A real estate model with many fields"
    _order = "id desc"
    active = fields.Boolean(string="Active", default="Active")
    bedrooms = fields.Integer(string="Bedrooms", default="2")
    best_price = fields.Float(
        string="Best Price", compute='_compute_best_price')
    buyer_id = fields.Many2one(
        'res.partner', string="Buyer", ondelete='restrict',
    )
    date_availability = fields.Datetime(
        string="Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3))
    description = fields.Text(string="Description")
    expected_price = fields.Float(string="Expected Price", required=True)
    facades = fields.Integer(string="Facades")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Float(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Direction",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        help="Type is used to specify the garden orientation"
    )
    garage = fields.Boolean(string="Garage")
    living_area = fields.Float(string="Living Area (sqm)")
    name = fields.Char(string="Title", required=True)
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id', string='Offers')
    postcode = fields.Char(string="Postcode")
    property_type_id = fields.Many2one(
        'estate.property.type', string="Property Type")
    salesman_id = fields.Many2one(
        'res.users', string="Salesman", ondelete='restrict',
    )
    selling_price = fields.Float(
        string="Selling Price", readonly=True, copy=False)
    sequence = fields.Integer(default=1)
    state = fields.Selection([('new', "New"),
                              ('offer_received', "Offer Received"),
                              ('offer_accepted', "Offer Accepted"),
                              ('sold', "Sold"),
                              ('cancelled', "Cancelled")
                              ],
                             default='new')
    tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Tags"
    )
    total_area = fields.Float(
        string="Total Area", compute='_compute_total_area'
    )
    visits_ids = fields.One2many(
        'estate.property.visit', 'property_id', string='Visits')
    visit_count = fields.Integer(
        compute='_compute_visit_count')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.mapped('offer_ids.price') or [0])

    @api.onchange('garden')
    def _onchange_garden(self):
        self.ensure_one()
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_property_sold(self):
        for rec in self:
            if rec.state == 'cancelled':
                raise UserError(_('A cancelled property cannot be sold'))
            if not rec.buyer_id or not rec.salesman_id:
                raise UserError(
                    _('Cant sell the property if it has no buyer or seller'))
            if rec.selling_price <= 0:
                raise UserError(
                    _('We don\'t do charity here. Set a proper selling price.'))
            rec.state = 'sold'
        return True

    def action_property_cancelled(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError(_('A sold property cannot be cancelled'))
            else:
                rec.state = 'cancelled'
        return True

    def action_select_best_offer(self):

        for rec in self:

            best_offer = self.env['estate.property.offer'].search(
                domain=[
                    ('property_id', '=', rec.id),
                    ('price', '=', rec.best_price),
                ],
                limit=1,
            )

            best_offer.action_status_accepted()

    def action_auto_refuse(self):
        for rec in self:
            threshold = 90 * rec.expected_price / 100
            below_par_offers = self.env['estate.property.offer'].search(
                domain=[
                    ('property_id', '=', rec.id),
                    ('price', '<', threshold),
                    ('status', '!=', False)
                ])

            below_par_offers.write({'status': 'refused'})

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be strictly positive.'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be positive.'
    )

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price != 0:
                percentage = rec.selling_price * 100 / rec.expected_price
                if percentage <= 10:
                    raise ValidationError(_(
                        'Selling price cannot be lower than 90 percent of expected price'))

    @api.ondelete(at_uninstall=False)
    def _check_state_before_deletion(self):
        for rec in self:
            if rec.state not in ('new', 'cancelled'):
                raise UserError(_(
                    "Cannot delete this record because it has active orders"))

    @api.depends('visits_ids')
    def _compute_visit_count(self):
        for rec in self:
            rec.visit_count = len(rec.visits_ids)

    def action_redirect_to_visits(self):
        view = 'estate.test_property_visits_action'
        action = self.env['ir.actions.act_window']._for_xml_id(view)
        action['view_mode'] = 'calendar'
        action['domain'] = [('agent_id', 'in', self.env.uid)]
        return action
