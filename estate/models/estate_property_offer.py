from odoo import fields, models, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for the property'

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.users', required=True, default=lambda self: self.env.user)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _offer_price_strictly_positive = models.Constraint(
        'CHECK(price > 0)',
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.now() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            deadline = datetime(record.date_deadline.year, record.date_deadline.month, record.date_deadline.day)
            record.validity = int((deadline - fields.Datetime.now()).days)

    def accept_offer(self):
        for record in self:
            if not record.property_id.offer_accepted:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
                record.property_id.offer_accepted = True 
            else:
                raise(UserError("Can not accept more than one offer"))
    
    def reject_offer(self):
        for record in self:
            record.status = 'refused'
