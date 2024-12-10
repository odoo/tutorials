from odoo import models, fields, api
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    living_area = fields.Float(string="Living Area (sqm)")
    garden_area = fields.Float(string="Garden Area (sqm)")
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)


