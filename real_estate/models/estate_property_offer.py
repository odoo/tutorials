from odoo import api, models, fields # type: ignore
from datetime import date
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float(required=True)
    status= fields.Selection(
        [('accepted', 'Accepted'),('refused','Refused')],
        string="Status",
        copy=False        
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property Name", required=True)

    validity= fields.Integer(compute="_compute_validity", inverse="_compute_date_deadline",string="Valid for", default=7)
    date_deadline= fields.Date(string="Offer Deadline ", default=date.today()+relativedelta(days=+7))

    @api.depends("date_deadline")
    def _compute_validity(self):
        for record in self:
            record.validity = (record.date_deadline-record.create_date.date()).days

    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date.date() + relativedelta(days=+(record.validity))


