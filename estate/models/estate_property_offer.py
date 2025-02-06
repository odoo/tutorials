from odoo import fields, models, api
from dateutil.relativedelta import relativedelta



class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for property"

    price = fields.Float()
    status= fields.Selection(
        selection=[("accepted","Accepted"), ("refused","Refused")],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property',required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline",inverse="_inverse_date_deadline", store=True)
    

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                # Ensure create_date is available and compute date_deadline
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                # If date_deadline is set, compute validity
                    delta = record.date_deadline - fields.Date.today()
                    record.validity = delta.days
            else:
                record.validity=7