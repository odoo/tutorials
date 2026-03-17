from odoo import models, fields ,api 
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'


    price = fields.Char(required = True)
    status = fields.Selection(
         selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
            ]
        , copy= False 
    )

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", 
        compute='_compute_date_deadline', 
        inverse='_inverse_date_deadline'
    )

   

    partner_id = fields.Many2one(comodel_name='res.partner' , string="Partner")
    property_id = fields.Many2one(comodel_name='estate.property' , string="Property")



    _check_price =  models.Constraint(
        'CHECK(price > 0)', "The offer price must be strictly positive.")


    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            date_start = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(date_start, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date_start = record.create_date.date() if record.create_date else fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - date_start).days
            else:
                record.validity = 7

    def action_accept(self):
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                    raise UserError("An offer has already been accepted for this property!")

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id


        return True
    
    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
