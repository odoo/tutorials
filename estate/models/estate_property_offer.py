from odoo import fields, models ,api
from datetime import datetime, timedelta 
from odoo.exceptions import UserError,ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    
    
    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('Accepted', 'Accepted'),
            ('Refused', 'Refused'),
        ],
        string="Status"
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    deadline_date = fields.Date(compute="_compute_validity", inverse="_inverse_validity",store=True)
    created_date = fields.Date(default=lambda self: datetime.today())
    accepted = fields.Boolean(default=False)

    @api.depends("validity", "created_date")
    def _compute_validity(self):
        for record in self:
            if record.created_date:
                record.deadline_date = record.created_date + timedelta(days=record.validity)
            else:
                record.deadline_date = False
                
    @api.depends("created_date", "deadline_date")
    def _inverse_validity(self):
        for record in self:
            if record.deadline_date and record.created_date:
                record.validity = (record.deadline_date - record.created_date).days
            else:
                record.validity = 0
    
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price <= 0  :
                raise ValidationError("The offer price must be greater than zero.")
    
    def action_accept(self):
        for record in self:
            if record.property_id.buyer :
               raise UserError("You can not accept offer it is already accepted ")
            else:
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            if record.property_id.buyer == record.partner_id:
                record.property_id.buyer = None
            else:
                raise UserError("You cannot reject this offer")
    # def action_refuse(self):
    #         if self.property_id.buyer == self.property_id:
    #             self.property_id.buyer = None
    #             self.property_id.selling_price = 10000
    #         else:
    #            raise UserError("You can not reject the offer")




