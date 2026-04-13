from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = "price desc"
    _check_offer = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive',
    )
    price = fields.Float(string="Price")
    margin = fields.Float(string="Margin", compute="_compute_margin", store=True)
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
            ('pending', "Pending")
        ],
        string="Status",
        copy=False,
        readonly=True,
        default='pending',
    )

    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', required=True, string="Property")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True, string="Property Type")

    validity = fields.Integer(string="Validity (days)", default=7, help='Number of days the offer is valid for')

    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", help="Deadline for the offer based on the validity period")

    spam_offer = fields.Boolean(related="property_id.spam", string="Spam offer")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = start + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start).days

    def action_accept(self):
        if self.property_id.state == 'sold':
            raise UserError(_("you cant accept a sold property"))
        self.status = 'accepted'
        other = self.property_id.offer_ids - self
        other.write({'status': 'refused'})
        self.property_id.state = 'offer_accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price

    def action_reject(self):
        if self.property_id.state == 'sold':
            raise UserError(_("You cant reject a sold property"))
        self.status = 'refused'

    @api.depends("price", "property_id.expected_price")
    def _compute_margin(self):
        for record in self:
            record.margin = record.price - record.property_id.expected_price

    # @api.model
    # def create(self, vals_list):
    #     records = super().create(vals_list)
    #     for record in records:
    #         prop = record.property_id
    #         suspicious_tag = self.env['estate.property.tag'].search([('name', '=', 'suspicious')])
    #         if not suspicious_tag:
    #             suspicious_tag = self.env['estate.property.tag'].create({'name': 'suspicious', 'color': 1})
    #         offers = prop.offer_ids
    #         if len(offers) == 3:
    #             times = offers.mapped('create_date')
    #             if times and max(times) - min(times) < timedelta(minutes=5):
    #                 prop.tag_ids |= suspicious_tag
    #                 for offer in prop.offer_ids:
    #                     offer.spam_offer = True
    #     return records

    @api.model
    def create(self, val_list):
        for val in val_list:
            prop = val.get('property_id')
            price = val.get('price')
            property_record = self.env['estate.property'].browse(prop)
            property_record.state = 'offer_received'
            if price < property_record.best_price:
                raise UserError(_("The new offer cant be less that existing best offer"))
        return super().create(val_list)
