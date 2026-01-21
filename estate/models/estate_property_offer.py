from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
import datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_validity", readonly=False)


    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for r in self:
            create = r.create_date.date() if isinstance(r.create_date, datetime.datetime) else fields.Date.today() 
            r.date_deadline = create + relativedelta(days=r.validity)

    
    def _inverse_validity(self):
        for r in self:
            create = r.create_date.date() if isinstance(r.create_date, datetime.datetime) else fields.Date.today()
            r.validity = (r.date_deadline - create).days
