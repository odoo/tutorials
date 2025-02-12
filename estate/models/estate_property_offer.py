from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    
    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive'),
        ('one_offer_per_buyer', 'UNIQUE(partner_id, property_id)', 'Buyer can only place one offer')
    ]
    
    price=fields.Float(string="Price")
    status=fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id=fields.Many2one(comodel_name="res.partner", required=True)
    property_id=fields.Many2one(comodel_name="estate.property", required=True, ondelete="cascade")
    validity=fields.Integer(string="Validity", default=7)
    date_deadline=fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id=fields.Many2one(related="property_id.property_type_id", store=True)
    
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            property.state = "offer_received"
            
            best_offer = self.search([('property_id', '=', vals['property_id'])], order="price desc", limit=1)
            
            if best_offer and best_offer.price > vals['price']:
                raise UserError(f"The offer price must be higher than {best_offer.price}")
        
        return super().create(vals_list)

    def unlink(self):
        print(self)
        properties = self.mapped("property_id")
        res = super().unlink();
        
        for property in properties:
            linked_offers = self.search_count([('property_id', '=', property.id)])
            
            if linked_offers == 0:
                property.state = 'new'
                property.buyer = ''
                property.selling_price = 0
        return res
    
    def action_accept_offer(self):
        if self.property_id.state == 'cancelled':
            raise UserError("This property is already cancelled")
        
        self.status = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        
        remaining_offers = self.search([
            '&',
            ('property_id', '=', self.property_id.id),
            ('id', '!=', self.id)
        ])
        if remaining_offers:
            remaining_offers.write({'status': 'refused'})
        
        return True

    def action_refuse_offer(self):
        self.status = "refused"
        return True
