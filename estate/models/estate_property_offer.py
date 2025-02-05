from dateutil.relativedelta import relativedelta
from odoo import fields,models,api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[
        ('accepted','Accepted'),
        ('refused','Refused')],
        string="Status",
        copy=False)
    partner_id = fields.Many2one("res.partner",string="Partner")
    property_id = fields.Many2one("estate.property",string="Property")
    validate = fields.Integer(string="Validity(days)",default=7)
    date_deadline = fields.Date(string="Deadline",default=fields.Date.today(),compute="_compute_deadline",inverse="_update_validity")

    #Function of implementing comptue field and inverse function on validity days and date dadeline
    @api.depends("validate","create_date")
    def _compute_deadline(self):
        for date in self:
            if date.create_date:
                date.date_deadline = date.create_date + relativedelta(days=date.validate)
            else:
                date.date_deadline = fields.Date.today() + relativedelta(days=date.validate)

    def _update_validity(self):
        for days in self:
            if days.date_deadline:
                days.validate = (days.date_deadline - fields.Date.today()).days
            else:
                days.validate = 7

