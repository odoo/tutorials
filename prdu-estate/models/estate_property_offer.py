from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "You receive: Northing. I receive: a goddamn house."
    price = fields.Float()
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if (record.create_date is None):
                record.date_deadline = fields.Date.now() + record.validity
                continue
            record.date_deadline = relativedelta(days=record.validity) + record.create_date

    def _inverse_date_deadline(self):
        for record in self:
            if (record.create_date is None):
                record.validity = record.date_deadline - fields.Date.now()
                continue
            record.validity = (record.date_deadline - record.create_date.date()).days
            
    def action_offer_accept(self):
        for record in self:
            record.status = "accepted"
            re_property = record.property_id
            re_property.selling_price = record.price
            re_property.customer_id = record.partner_id
            
    def action_offer_refuse(self):
        for record in self:
            record.status = "refused"
