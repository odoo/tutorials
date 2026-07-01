from odoo import fields, models, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('Accepted', "Accepted"),
            ('Refused', "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity date", default=7)
    date_deadline = fields.Date(string="Deadline date", compute="_compute_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            #breakpoint()
            base = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base + timedelta(record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = record.base + timedelta(record.date_deadline)
