from datetime import timedelta
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer model"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused'),
        ])
    partner_id = fields.Many2one("res.partner",required=True)
    property_id = fields.Many2one(comodel_name="estate.property",required=True)  
    validity = fields.Integer(string="Valid till (Days)",default=7)
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", store=True)

    @api.depends( "property_id.create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = record.property_id.create_date + timedelta(days=record.validity) if record.property_id.create_date else None
            

    def _inverse_deadline(self): 
        for record in self:
            if record.deadline:
                create_date = record.property_id.create_date.date()
                record.validity = (record.deadline - create_date).days
                record.validity = max(record.validity, 0)
