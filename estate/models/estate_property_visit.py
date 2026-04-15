from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyVisit(models.Model):
    _name = "estate.property.visit"
    _description = "Property Visit"

    property_id = fields.Many2one("estate.property")
    partner_id = fields.Many2one(
        "res.partner", string="Customer"
    )
    visit_time = fields.Datetime(string="Visit Time", required=True)

    @api.constrains('visit_date', 'property_id')
    def _check_visit_time(self):
        for record in self:
            for visit in record.property_id.visit_ids:
                if record.id == visit.id or record.visit_time.date() != visit.visit_time.date():
                    continue
                if self.partner_id == self.partner_id and record.visit_time == visit.visit_time:
                    raise UserError("CAN'T VISIT 2 PROPERTIES AT SAME TIME")
                if record.visit_time - visit.visit_time < timedelta(hours=1):
                    raise UserError("THIS SLOT IS BOOKED")
