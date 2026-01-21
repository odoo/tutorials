from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


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
            if r.create_date is not None:
                r.date_deadline = r.create_date.date() + relativedelta(days=r.validity)

    
    def _inverse_validity(self):
        for r in self:
            if r.create_date is not None:
                r.validity = (r.date_deadline - r.create_date.date()).days


