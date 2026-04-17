from datetime import timedelta
from odoo import api, fields, models


class EstatePropertyVisit(models.Model):
    _name = "estate.property.visit"
    _description = "Property Visits"
    _rec_name = "partner_id"

    property_id = fields.Many2one("estate.property", string="Property")
    partner_id = fields.Many2one("res.partner", string="Customer")
    visit_date = fields.Datetime(required=True)
    stato = fields.Selection(
        selection=[
            ('scheduled', "Scheduled"),
            ('done', "Done"),
        ],
        default='scheduled'
    )

    _unique_date = models.Constraint(
        'UNIQUE(property_id, visit_date)',
        'Already Scheduled!!',
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            self.env['calendar.event'].create({
                'name': "Visit",
                'start': record.visit_date,
                'stop': record.visit_date + timedelta(hours=1),
            })
        return records
