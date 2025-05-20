from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Model to modelize Offer for Properties"

    price = fields.Float()
    status= fields.Selection(
        string='Status',
        selection=[('accepted','Accepted'), ('refused','Refused')],
        help="The Status of the offer"
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity =  fields.Integer(default=0, string="Validity (days)")
    date_deadline = fields.Datetime(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            computation_date = record.create_date if record.create_date else fields.date.today()
            record.date_deadline = computation_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.date_deadline = (record.date_deadline - record.create_date).days