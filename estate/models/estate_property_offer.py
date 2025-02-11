from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = 'price desc'

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            record.validity = (record.deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            if(record.status == 'accepted'):
                raise UserError('Offer Already accepted')
            else:
                record.status = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.status = 'offer_accepted'
                other_property = record.property_id.offer_ids.filtered(lambda offer: offer.id != record.id)
                other_property.write({'status' : 'refused'})
        
    def action_refuse_offer(self):
        for record in self:
            if(record.status == 'refused'):
                raise UserError('Offer Already refused')
            else:
                record.status = 'refused'
    
    _sql_constraints =[
        ('_check_price','CHECK(price > 0)','Offer Price must be positive'),
    ]
    
    price = fields.Float()
    validity = fields.Integer("Validity (days)", default=7)
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_validity")
    status = fields.Selection(
        selection=[("accepted","Accepted"), ("refused","Refused")], copy=False, readonly=True
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
