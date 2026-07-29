from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "price desc"

    price = fields.Float(string="Price")
    _check_offer_price = models.Constraint(
        'CHECK( price>=0 )',
        'offer price cannot be less than 0 or in negative value ',
    )
    status = fields.Selection(
        selection=[
            ('Accepted', "Accepted"),
            ('Refused', "Refused"),
        ],
        string="Status",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type Id", store=True)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity date", default=7)
    is_spam = fields.Boolean(string="spam", default=False, copy=False)

    @api.constrains('partner_id')
    def _check_spam(self):
        for offer in self:
            count = self.search_count([
                ('partner_id', '=', offer.partner_id.id),
                ('create_date', '>=', fields.Datetime.now() - timedelta(minutes=5)),
            ])
            if count > 5:
                self.search([
                    ('partner_id', '=', offer.partner_id.id),
                    ('create_date', '>=', fields.Datetime.now() - timedelta(minutes=5)),
                ]).write({'is_spam': True})

    date_deadline = fields.Date(
        string="Deadline date", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            #            breakpoint()
            base = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base + timedelta(record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - base).days

    def action_accept(self):
        if 'Accepted' in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("An offer has already been accepted for this property"))
        self.status = 'Accepted'
        self.property_id.state = 'offer_accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        (self.property_id.offer_ids - self).write({'status': 'Refused'})

    def action_refuse(self):
        self.status = 'Refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('property_id') and vals.get('price'):
                property = self.env['estate.property'].browse(vals['property_id'])
                if property.state == 'new':
                    property.state = 'offer_received'
        return super().create(vals_list)
