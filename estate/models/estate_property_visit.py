from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class Estatepropertyvisits(models.Model):
    _name = 'estate.property.visit'
    _description = "Estate Property Visit"

    name = fields.Char()
    property_id = fields.Many2one('estate.property')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date = fields.Datetime(string='Scheduled At', required=True)

    @api.constrains('date', 'property_id')
    def _check_visit_time(self):
        for rec in self:
            for visit in rec.property_id.visit_ids:
                if visit.id == rec.id:
                    continue
                if rec.date < visit.date + timedelta(hours=1) and rec.date > visit.date - timedelta(hours=1):
                    raise UserError("Both the visit cannot have Same time and it must be greater than 1 hr")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.date:
                self.env['calendar.event'].create({
                    'name': "property check in",
                    'start': record.date,
                    'stop': record.date + timedelta(hours=1),
                })
        return records
