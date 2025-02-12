from odoo import api,fields, models
from datetime import datetime,timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"

    price = fields.Float()
    state = fields.Selection(
        selection = [('accepted','Accepted'),('refused','refused')]
    )
    partner_id = fields.Many2one('res.partner',required=True)
    property_id = fields.Many2one('estate.property',required=True)
    property_type_id  = fields.Many2one(related='property_id.property_type_id', store=True)    
    validity = fields.Integer(default=7)
    deadline = fields.Date(compute="_compute_date_deadline",inverse="_inverse_deadline",store=True)
    
    _sql_constraints = [('price_pos','check(price>0)','price should be positive!')]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.deadline = record.create_date.date()+ timedelta(days=record.validity)
            else:
                record.deadline = fields.date.today()+ timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.deadline:
                record.validity = (record.deadline - record.create_date.date()).days

    def action_offer_accept(self):
        
        for record in self:
            
            if(record.state=="accepted"):
                raise UserError('Offer is already accepted')
            else:
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.status = 'offer_accepted'
                record.state = "accepted"
                other_offer = record.property_id.offer_ids.filtered(lambda offer : record.id!=offer.id)
                other_offer.write({'state':'refused'})

    def action_offer_reject(self):
        for record in self:
            if record.state == 'refused':
                raise UserError('Offer is already refused')
            else:
                record.state = "refused"
                record.property_id.selling_price = False
                record.property_id.buyer_id = False
