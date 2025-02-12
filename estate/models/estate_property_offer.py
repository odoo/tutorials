from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Model for offers for each property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused'),
        ])
    partner_id = fields.Many2one("res.partner",required=True)
    property_id = fields.Many2one("estate.property",required=True)  
    validity = fields.Integer(string="Valid till (Days)",default=7)
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", store=True)

    @api.depends("property_id.create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = record.property_id.create_date + timedelta(days=record.validity) if record.property_id.create_date else fields.Date.today()
            

    def _inverse_deadline(self): 
        for record in self:
            if record.deadline:
                record.validity = max((record.deadline - record.property_id.create_date.date()).days, 0)


    def action_accept(self):
        for record in self:
            if record.property_id.state == "sold":
                raise UserError("A sold property cannot accept new offers!")
            
            record.property_id.offer_ids.filtered(lambda o: o.status == "accepted").write({'status': 'refused'})            
            record.status = 'accepted'
            record.property_id.partner_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"


    def action_refuse(self):
        for record in self:
            record.status = 'refused'
