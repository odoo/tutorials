from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatepropertyVisit(models.Model):
    _name = 'estate.property.visit'
    _description = "Property Visits"

    property_id = fields.Many2one("estate.property")
    buyer_id = fields.Many2one("res.partner", required=True)
    visit_date = fields.Datetime(string="Visit Date")
    stop_date = fields.Datetime(string="Stop date")
    state = fields.Selection(selection=[
        ('Scheduled', "Scheduled"),
        ('Done', "Done")
    ],
    default="Scheduled")

    @api.constrains('visit_date', 'property_id')
    def _check_visit_time(self):
        for record in self:
            for visit in record.property_id.visit_ids:
                if record.id == visit.id or record.visit_date.date() != visit.visit_date.date():
                    continue
                if record.visit_date - visit.visit_date < timedelta(hours=1):
                    raise UserError("Visit alredy scheduled for this time-slot!!")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            self.env['calendar.event'].create({
                'name': f"Visit: {record.property_id.name} - {record.buyer_id.name}",
                'start': record.visit_date,
                'stop': record.stop_date
            })
        return records
