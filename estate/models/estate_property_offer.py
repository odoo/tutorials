# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions
from odoo.tools import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(string="Offer Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'The price must be strictly positive.')
    ]

    @api.depends('validity', 'create_date')
    def _compute_deadline_date(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.to_date(record.create_date) + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda r: r.status == 'accepted'):
                raise exceptions.UserError("Another offer is already accepted on this property.")
            record.status = 'accepted'
            record.property_id.accept_offer(record.price, record.partner_id)
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
