from odoo import fields,models,api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate properties offers"

    price = fields.Float("Price",required=True)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        help="This selection is used to tell whether  buying offer is accepted or refused"
    )
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.property')

    validity = fields.Integer(default=7)
    create_date = fields.Date(default=fields.Date.today())
    date_deadline = fields.Date(compute='_compute_deadline',inverse='_inverse_validity')

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The offer price has to be > 0'),
    ]

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today()+ relativedelta(days=record.validity)
            
    def _inverse_validity(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.date_deadline = (record.date_deadline - fields.Date.today()).days

    def action_confirm_offer(self):
        for record in self:
            if not record.status:
                record.status = 'accepted'              
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

        return True
    
    def action_refuse_offer(self):
        for record in self:
            if not record.status:
                record.status = 'refused'  
        return True