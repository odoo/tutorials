from odoo import fields, models,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
     _name = 'estate.property.offer'
     _description = 'real estate property offer'
     price = fields.Float()
     _order = 'price desc'
     status = fields.Selection(
        selection=[
        ('accepted','Accepted'),
        ('rejected','Rejected'),],
        copy=False
     )
     partner_id = fields.Many2one('res.partner', required=True)
     property_id = fields.Many2one('estate.property', required=True)
     validity = fields.Integer("Validity", default=7)
     date_deadline = fields.Date("Date Dealine",compute="_compute_date_deadline" ,  inverse="_inverse_date_deadline")
     property_type_id = fields.Many2one(related='property_id.property_type_id' , store = True)
     
     _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]
     
     @api.depends('validity')
     def _compute_date_deadline(self):
         for record in self:
            current_date = fields.Date.today()
            record.date_deadline = current_date + relativedelta(days=record.validity)
    
     @api.model_create_multi
     def create(self, vals_list):
         records = super().create(vals_list)
         for vals in vals_list:
                prop_id = vals.get('property_id')
                offer_price = vals.get('price')
                res = self.env["estate.property"].browse(prop_id)
                if prop_id:
                    res.write({'state': "offer_received"})
                    if offer_price:
                        existing_offers = self.search(
                        [("property_id", "=", prop_id), ("price", ">", offer_price)],
                        limit=1,
                    )
                    if existing_offers:
                       raise UserError( "An offer with the higher price already exists.")
         return records

     def _inverse_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            if record.date_deadline:
                record.validity = relativedelta(record.date_deadline, current_date).days

     def set_offer_rejected(self):
         for record in self:
             record.status = "rejected"
         return True
     
     def set_offer_accepted(self):
        for record in self:
             record.status = "accepted"
             record.property_id.state = "offer_accepted"
             record.property_id.selling_price = record.price
             record.property_id.buyer_id = record.partner_id

        other_offer = self.env['estate.property.offer'].search([

            ('property_id' , '=' , self.property_id.id),
            ('id' , '!=' , self.id),
            ('status' , '!=' , 'rejected')  
        ])
        other_offer.write({'status' : 'rejected'})
        return True
