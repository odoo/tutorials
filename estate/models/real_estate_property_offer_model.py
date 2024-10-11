
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import datetime



class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"

    price = fields.Float()
    status = fields.Selection( 
        string = 'Status',
        selection = [('accepted','Accepted'),('refused','Refused')],
        copy = False
    )
    partner_id = fields.Many2one('res.partner',string = "Buyer", required=True)
    property_id = fields.Many2one('estate.property',string="Property", required=True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = '_compute_deadline', inverse = "_inverse_validity", store=True)


    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                # print("Hfedfdfdfi", record.id,record.create_date)
                # print(record.create_date.date() + relativedelta(days=record.validity))
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + relativedelta(days=record.validity)
        # print(record.create_date, "Hi")




    def _inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days


    def action_offer(self):

        return True

    