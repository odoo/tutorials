from odoo import fields, models, api


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_compute_validity", string="Deadline")

    @api.depends("create_date","validity")
    def _compute_date_deadline(self):
        for record in self:
            created_at = record.create_date or fields.Date.today()
            record.date_deadline=fields.Date.add(created_at,days=self.validity)
    
    def _compute_validity(self):
        for record in self:
            created_at = record.create_date or fields.Date.today()
            delta = record.date_deadline - created_at.date()
            record.validity = delta.days
