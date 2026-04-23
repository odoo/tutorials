from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyVisit(models.Model):
    _name = "estate.property.visit"
    _description = "Schedule for properties"

    salesperson_id = fields.Many2one(related="property_id.salesperson_id")
    customer_name = fields.Many2one('res.partner')
    visit_date = fields.Datetime(default=fields.Datetime.now())
    property_id = fields.Many2one('estate.property', required=True)

    @api.model_create_multi
    def create(self, vals_list):

        visits = super().create(vals_list)

        for visit in visits:
            stop_time = visit.visit_date + timedelta(hours=+1)
            self.env['calendar.event'].create({
                'name': 'Property Visit',
                'start': visit.visit_date,
                'stop': stop_time,
            })

        return visits

    @api.constrains('visit_date', 'property_id')
    def _check_visit_time(self):
        for record in self:
            for visit in record.property_id.visit_ids:
                if record.id == visit.id or record.visit_date.date() != visit.visit_date.date():
                    continue
                if record.visit_date - visit.visit_date < timedelta(hours=1):
                    raise UserError("2 visits cannot have same time")
