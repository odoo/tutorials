from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused'), ('pending', 'Pending')],
        default='pending',
    )

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    create_date = fields.Datetime(readonly=True, default=fields.Datetime.now)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_deadline',
        inverse='_inverse_deadline',
        string="Deadline")

    @api.depends('validity')
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Datetime.now()) + relativedelta(days=offer.validity)

    # Despite what the docs say, I couldn't get this to update without `onchange`
    @api.onchange('date_deadline')
    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days
