from odoo import fields, models, api, exceptions
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate properties offer"
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'),
        ('refused', 'Refused')],
        help="Status of the offer",
        copy=False)
    validity = fields.Integer('Validity (days)', default='7')
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    # base_date = fields.Date() # This is temporory date field for type conversion.

    _sql_constraints = [
        ('check_offered_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - base_date.date()).days
    
    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.status = 'refused'
            record.property_id.selling_price, record.property_id.buyer, record.property_id.state = record.price, record.partner_id, 'offer accepted'
                
    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = 1
            record.status = 'refused'
