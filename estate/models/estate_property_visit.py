from odoo import api, fields, models


class EstatePropertyVisit(models.Model):
    _name = "estate.property.visit"
    _description = "Property Description"

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    propert_id = fields.Many2one("estate.property", string="Property", required=True)
    visit_date = fields.Datetime(string="Visiting Date")
    end_date = fields.Datetime(string="End date")
    # time_from = fields.Float(string='Hour from')
    # time_to = fields.Float(string='Hour to')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            self.env['calendar.event'].create({
                'name': "property visit",
                'start': record.visit_date,
                'stop': record.end_date,
            })
        return records
