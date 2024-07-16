from datetime import timedelta

from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[('accepted', "Accepted"), ('rejected', "Rejected")],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string="Partner ID", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Date Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    @api.depends('create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date is False:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
            else:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    @api.onchange('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

