import logging
from dateutil import relativedelta as rd

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


_logger = logging.getLogger(__name__)


def _get_availability_date(self):
    # _logger.info("!!! %s", self)
    return fields.Date.today() + rd.relativedelta(months=3)


def _get_salesperson(self):
    # _logger.info(self.env.user.name)
    # _logger.info(self.env.user.id)
    # _logger.info(self.env.user)
    return self.env.user


class EstateProperties(models.Model):
    _name = 'estate.properties'
    _description = 'Real Estate Properties'
    _inherit = ['mail.thread']
    _order = 'sequence'

    active = fields.Boolean(help="Should the property be listed?", default=True)
    bedrooms = fields.Integer(default=2)
    best_price = fields.Float(compute='_compute_best_price')
    buyer_id = fields.Many2one(comodel_name='res.partner', copy=False)
    commission = fields.Integer(compute='_compute_commission', store=True)
    date_availability = fields.Date(string="Availability Date", copy=False, default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3))
    description = fields.Text()
    expected_price = fields.Float(string="Expected Price", required=True)
    facades = fields.Integer()
    garage = fields.Boolean(string="Has Garage?", help="Does the proeprty have a garage?")
    garden = fields.Boolean(string="Has Garden?", help="Does the property have a garden?")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        help="Directional orientation of the garden of the property shown"
    )
    invoice_count = fields.Integer(default=0)
    living_area = fields.Integer()
    name = fields.Char(string="Property Name", required=True)
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id')
    postcode = fields.Char()
    potential_buyer_count = fields.Integer(compute='_compute_potential_buuyers')
    price_gap = fields.Float(compute='_compute_price_gap')
    property_type_colour = fields.Selection(related='property_type_id.colour', readonly=False)
    property_type_id = fields.Many2one(comodel_name='estate.property.type')
    reminder_sent = fields.Boolean(default=False)
    property_visit_ids = fields.One2many(comodel_name='estate.property.visit', inverse_name='property_id')
    salesperson_id = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.user)
    # salesperson = fields.Char(default=_get_salesperson)
    selling_price = fields.Float(readonly=True, copy=False, tracking=True)
    sequence = fields.Integer()
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        required=True, default='new', copy=False, string="Status"
    )
    tag_ids = fields.Many2many(comodel_name='estate.property.tag')
    total_area = fields.Integer(compute="_compute_total_area")
    visit_count = fields.Integer(compute='_compute_visit_count')

    _check_expected_price = models.Constraint(
        'CHECK (expected_price > 0 AND selling_price >= 0)',
        "Price should strictly be positive",
    )

    @api.depends('property_visit_ids')
    def _compute_visit_count(self):
        for property in self:
            property.visit_count = len(property.property_visit_ids)

    @api.depends('buyer_id')
    def _compute_potential_buuyers(self):
        property_buyers = self.env['estate.properties'].search([
            ('buyer_id', '!=', False)
        ])
        partners_detected = property_buyers.mapped('buyer_id')
        current_user = self.env.user.partner_id
        for property in self:
            if current_user in partners_detected:
                property.potential_buyer_count = len(partners_detected) - 1
            else:
                property.potential_buyer_count = len(partners_detected)

    @api.constrains('selling_price')
    def _check_selling_price(self):
        # breakpoint()
        # _logger.error(self.id)
        for property in self:
            sp_threshold = 0.9 * property.expected_price
            # _logger.error(sp_threshold)
            # _logger.error(property.selling_price)
            # _logger.error(property.expected_price)
            # _logger.error(property.id)
            if property.selling_price < sp_threshold:
                raise ValidationError("Selling price cannot be less than 90% of the expected price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        # _logger.error(self)
        for property in self:
            # _logger.error(property._fields)
            # _logger.error(property)
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            # _logger.error(self.mapped('offer_ids.price'))
            offer_prices = property.mapped('offer_ids.price')
            # _logger.error(offer_prices)
            # _logger.error(max(offer_prices))
            property.best_price = max(offer_prices) if offer_prices else 0

    # @api.constrains('expected_price')
    # def _check_expected_price(self):
    #     for property in self:
    #         if property.expected_price < 0:
    #             raise UserError("Value cannot be less than zero.")

    @api.onchange('garden')
    def _onchange_garden(self):
        # _logger.error(self.garden)
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # @api.constrains('date_availability')
    # def _check_date_availability(self):
    #     for property in self:
    #         if property.date_availability < fields.Date.context_today(property):
    #             raise ValidationError("Past dates not allowed")

    @api.depends('best_price', 'expected_price')
    def _compute_price_gap(self):
        for property in self:
            if property.best_price and property.expected_price:
                property.price_gap = property.best_price - property.expected_price
            else:
                property.price_gap = 0

    @api.onchange('state')
    def _onchnage_state(self):
        if self.state == 'cancelled':
            self.active = False
        else:
            self.active = True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_state(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise UserError("Cannot delete property")

    def property_cancelled(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError("Property already cancelled")
            elif property.state != 'sold':
                property.state = 'cancelled'
                property.active = False
            else:
                raise UserError("A sold property cannot be cancelled")
        return True

    def action_quotation_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """

    def property_sold(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("Property already sold")
            elif property.state != 'cancelled':
                if property.buyer_id:
                    property.state = 'sold'
                else:
                    raise UserError("No buyer for this property yet")
            else:
                raise UserError("A cancelled property cannot be sold")
            # sep_ids = self.buyer_id.ids + self.salesperson_id.ids

            template = self.env.ref('estate.estate_property_sold_mail_template')
            ctx = {
                    'default_model': 'estate.properties',
                    'default_partner_ids': [self.buyer_id.id, self.salesperson_id.partner_id.id],
                    'default_res_ids': self.ids,
                    'default_template_id': template.id,
                    'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
                }

            return {
                    'name': ('Send'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'mail.compose.message',
                    'views': [(False, 'form')],
                    'view_id': False,
                    'target': 'new',
                    'context': ctx,
                }

    @api.depends('selling_price')
    def _compute_commission(self):
        for property in self:
            if property.selling_price:
                property.commission = property.selling_price * 0.06

    def property_accept(self):
        # breakpoint()
        # best_offers = []
        # for property in self.offer_ids:
        #     best_offers.append(property.price)
        #     _logger.error(best_offers)
        # property_to_accept = max(best_offers)
        # _logger.error(property_to_accept)
        # if self.offer_ids:
        #     best = self.offer_ids.search([('price', '=', self.best_price), ('status', 'not in', ['refused'])])
        #     if best:
        #         best.offer_accepted()
        #         return
        #     best = self.offer_ids.search([('price', '<', self.best_price), ('status', 'not in', ['refused'])], 0, 1, order='price DESC')
        #     best.ensure_one()
        #     best.offer_accepted()
        #     # _logger.error(best)
        # else:
        #     raise ValidationError("No offers listed for this property")
        # for property in self.offer_ids:
        #     if property.status == 'accepted':
        #         pass
        #     else:
        #         property.status = 'refused'
        self.ensure_one()
        best_offer = self.offer_ids.filtered(lambda offer: offer.status not in ['accepted', 'refused'])

        if not best_offer:
            raise ValidationError("No offers listed for this property")

        best_offer = best_offer.sorted(lambda offer: offer.price, reverse=True)[0]
        return best_offer.offer_accepted()

    @api.onchange('offer_ids')
    def offer_received_state(self):
        if self.offer_ids and self.state == 'new':
            self.state = 'offer_received'

    def action_potential_buyers(self):
        # _logger.error("Hellooooooooooooooooooooo")
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('base.action_partner_form')
        action['view_mode'] = 'list'
        action['views'] = []
        action['domain'] = [
            ('property_id', '!=', False)
        ]
        action['context'] = {
            'create': False,
            'edit': False,
            'delete': False,
        }
        return action

    def action_schedule_visit(self):
        if not self.buyer_id:
            raise ValidationError("No buyer set to visit the schedule")
        return {
            'name': 'Visit',
            'res_model': 'estate.property.visit',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'context': {
                'default_property_id': self.id,
                'default_property_title': self.display_name,
                'default_property_buyer': self.buyer_id.name,
            },
            'target': 'current',
            'type': 'ir.actions.act_window',
        }

    def show_visits(self):
        action = self.env["ir.actions.actions"]._for_xml_id("estate.estate_property_visit_action")  # type: ignore
        action['domain'] = [
            ('property_title', 'ilike', self.display_name),
        ]
        return action
