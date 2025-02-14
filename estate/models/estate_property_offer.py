from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = 'price desc'

    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_validity")
    price = fields.Float()
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer("Validity (days)", default=7)
    status = fields.Selection(
        selection=[("accepted","Accepted"), ("refused","Refused")], copy=False, readonly=True
    )

    _sql_constraints =[
        ('_check_price','CHECK(price > 0)','Offer Price must be positive'),
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = fields.Date.today() + relativedelta(days=record.validity) or record.create_date.date() + relativedelta(days=record.validity)
    
    def _inverse_validity(self):
        for record in self:
            record.validity = (record.deadline - record.create_date.date()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if property_id.offer_ids:
                max_offer = max(property_id.offer_ids.mapped('price'))
                if vals['price'] <= max_offer:
                    raise UserError("The offer price must be higher than the current maximum offer.")
            property_id.write({'status': 'offer_received'})
        return super().create(vals_list)

    def action_accept_offer(self):
        for record in self:
            if(record.status == 'accepted'):
                raise UserError('Offer Already accepted')
            else:
                record.status = 'accepted'
                record.property_id.write({'buyer_id' : record.partner_id, 'selling_price' : record.price, 'status': 'offer_accepted'})
                other_property = record.property_id.offer_ids.filtered(lambda offer: offer.id != record.id)
                other_property.write({'status' : 'refused'})
        
    def action_refuse_offer(self):
        for record in self:
            if(record.status == 'refused'):
                raise UserError('Offer Already refused')
            record.status = 'refused'
