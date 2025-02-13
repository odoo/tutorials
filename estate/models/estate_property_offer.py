from odoo import api,fields, models
from odoo.exceptions import UserError,ValidationError
from datetime import timedelta

class EstatePropertyTag(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted','Accepted'),
                    ('refused','Refused')],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Properties", required=True, ondelete="cascade")

    validity = fields.Integer(default="7")
    date_deadline = fields.Date(compute="_compute_date_deadline",inverse="_inverse_date_deadline",store=True)

    property_type_id = fields.Many2one("estate.property.type", string="Property Types", store=True)

    @api.depends("validity","create_date")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = timedelta(record.validity) + create_date.date()

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
