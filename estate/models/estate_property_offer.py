from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer object"

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_compute_validity")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    @api.depends("date_deadline")
    def _compute_validity(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
