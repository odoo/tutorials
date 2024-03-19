# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
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

    @api.depends('validity')
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
