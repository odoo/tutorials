from datetime import timedelta, datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


class estatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "This is offer table"
    _order = "id desc"

    price = fields.Float(required=True)
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    validity = fields.Integer(default=7, string="Validity")
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string="Date Deadline")
    sum = fields.Integer(compute='_compute_sum', string="Sum")
    sum2 = fields.Integer(compute='_compute_sum2', string="Sum2")

    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property')
    property_type_id = fields.Many2one(comodel_name="estate.property.type", related="property_id.property_type_id", store=True)
    
    _sql_constraints = [
            ('check_offer_price','CHECK(price > 0)','A property offer price must be strictly positive.')
    ]

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(record.validity)
            else:
                record.date_deadline = datetime.today() + timedelta(record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - datetime.today()).days

    @api.depends('validity')
    def _compute_sum(self):
        for record in self:
            record.sum = 7 + record.validity

    @api.depends('sum')
    def _compute_sum2(self):
        for record in self:
            record.sum2 = 7 + record.sum

    def action_accept(self):
        for record in self:
            if record.property_id.state in ['sold', 'offer accepted']:
                raise UserError("Already one offer is accepted.")
            if record.status == 'accepted':
                continue
            record.status = 'accepted'
            record.property_id.state = 'offer accepted'
            record.property_id.buyer_id = self.partner_id
            record.property_id.selling_price = self.price

    def action_refuse(self):
            if(self.status == 'accepted'):
                self.status = 'refused'
                self.property_id.buyer_id = False
                self.property_id.selling_price = False
            else: 
                self.status = 'refused'
    
    @api.model
    def create(self, offer):
        property_id = self.env["estate.property"].browse(offer["property_id"])
        if offer["price"] < max(property_id.offer_ids.mapped("price") + [0]):
            raise UserError("Offer price must be higher than existing offer.")
        property_id.state = "offer received"
        return super().create(offer)