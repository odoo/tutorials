from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError,UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for property"
    _order = "price desc"

    price = fields.Float()
    status= fields.Selection(
        selection=[("accepted","Accepted"), ("refused","Refused")],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete="cascade")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True, string="Property Type")
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)
                
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                    delta = record.date_deadline - fields.Date.today()
                    record.validity = delta.days
            else:
                record.validity=7      

    def action_accept(self):
        for record in self:
            if record.status == 'accepted' or record.status == 'refused':
                raise exceptions.UserError("Property is already accepted or refused.")
            else:
                all_offers = record.property_id.offer_ids  # Geting all offers of property
                for offer in all_offers:
                    if offer.id != record.id:  # Excluding the current offer
                        offer.status = 'refused'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer_accepted"
                record.status = 'accepted' 

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted' or record.status == 'refused':
                raise exceptions.UserError("Property is already accepted or refused.")
            else:
                record.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        
        for vals in vals_list:
            property_obj = self.env['estate.property'].browse(vals['property_id'])  

            best_offer_price = property_obj.best_price or 0  
            new_offer_price = vals.get('price', 0)  

            if new_offer_price < best_offer_price:
                raise UserError(f"The offer must be higher than the best offer ({best_offer_price}).")

            property_obj.write({'state': 'offer_received'})

        return super().create(vals_list)
