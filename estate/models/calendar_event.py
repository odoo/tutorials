from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    estate_visit_id = fields.Many2one('estate.property.visit')
    estate_property_id = fields.Many2one('estate.property')
