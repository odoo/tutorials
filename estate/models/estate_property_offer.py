from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"

    name = fields.Char(required=True)
    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            creation_date = (record.create_date or fields.Datetime.today()).date()
            record.date_deadline = fields.Date.add(creation_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            creation_date = (record.create_date or fields.Datetime.today()).date()
            record.validity = (record.date_deadline - creation_date).days
