# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    _inherit = ['rating.mixin', 'mail.thread', 'mail.activity.mixin', 'website.published.mixin']
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "Expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price > 0)", "Selling price must be strictly positive")  
    ]

    name = fields.Char(string="Title",tracking=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date availability", copy=False, default=fields.Date.today() + timedelta(days=+90))
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')
    ], string = "Garden Orientation", help = "It is used to define the garden orientation")
    state = fields.Selection([
        ('new', 'New'),
        ('offerreceived', 'Offer Received'),
        ('offeraccepted', 'Offer Accepted'), 
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string="State", default = "new", tracking=True)
    active = fields.Boolean("Active", default=True)
    seller_id = fields.Many2one(comodel_name="res.users", string="Salesperson")
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id", string="Offer Id")
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    best_offer = fields.Integer(string="Best Offer", compute="_compute_best_offer")
    reference = fields.Char(string="Reference", readonly=True, copy=False)
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company)
    rating_count = fields.Integer(string="Ratings count", compute="_compute_rating_count")
    property_image = fields.Image()

    # === COMPUTE METHODS === #
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in (self):
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)
    
    # === Constraints and Onchanges === #
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        if self.selling_price and self.selling_price < self.expected_price * 0.9:
            raise ValidationError(_("Selling price cannot be lower than 90% of the expected price."))

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.depends('message_ids.rating_value')
    def _compute_rating_count(self):
        """Compute the number of ratings for this property."""
        for record in self:
            record.rating_count = self.env['rating.rating'].search_count([
                ('res_model', '=', 'estate.property'),
                ('res_id', '=', record.id)
            ])

    # === CRUD Methods === #
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('estate.property') or '/'
        return super().create(vals)

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(_("You cannot delete a record which is %s" %record.state))

    # === Action Methods === #
    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("Cancelled properties cannot be sold"))
            elif record.state != "offeraccepted":
                raise UserError(_("No offers received yet") if record.state == "new"
                else _("Select an offer to sell the property"))
            else:
                record.state = "sold"

            template_id = self.env.ref("estate.estate_rating_template")
            if template_id:
                template_id.send_mail(record.id, force_send=True)
                
    def action_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("sold properties cannot be cancelled"))
            else:
                record.state = "cancelled"

    def action_open_add_offer(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Offer',
            'res_model': 'estate.property.offer.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('estate.estate_propety_offer_wizard_form').id,
            'target': 'new',
            'context': {'default_property_ids': [(6, 0, self.ids)]}
        }

    # Improvement Needed
    
    # def action_helper(self):
    #     # self.ensure_one()
    #     action = self.env['ir.actions.actions']._for_xml_id('estate.estate_property_action')
    #     domain = [('state', 'in', ['new', 'offerreceived', 'offeraccepted'])]
    #     total_available_properties = self.search(domain, limit=1)
    #     if total_available_properties == 0:
    #         action['help'] = self.env['ir.ui.view']._render_template(
    #             'estate.estate_property_action_helper'
    #         )
    #     return action

    def _track_subtype(self, vals):
        self.ensure_one()
        if 'state' in vals and self.state == 'offeraccepted':
            return self.env.ref('estate.mt_state_change')
        return super()._track_subtype(vals)
