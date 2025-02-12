# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused'),
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default="7", string="Validity (days)")
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
        'The offer price must be strictly positive'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
            else:
                create_date = fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
            else:
                create_date = fields.Date.today()
            record.validity = (record.date_deadline - create_date).days


    def accept_offer(self):
        rc = self.property_id.offer_ids.mapped('status')
        if not any(status=='accepted' for status in rc):
            for record in self:
                record.property_id.selling_price = record.price
                record.status='accepted'
                record.property_id.buyer = record.partner_id
                record.property_id.state = 'offer accepted'
        else:
            raise UserError(_("One of the offer is already accepted"))

    def refuse_offer(self):
        for record in self:
            record.status='refused'
