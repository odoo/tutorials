from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyVisit(models.Model):
    _name = 'estate.property.visit'
    _description = 'estate property visit'
    _order = 'date desc'
    _sql_const = models.UniqueIndex(
        '(date, property_id)',
        'This property is already booked for a visit on this date!',
    )

    property_id = fields.Many2one('estate.property', required=True)
    visitor_id = fields.Many2one('res.partner', required=True)
    date = fields.Date(required=True)
    comment = fields.Text()
    state = fields.Selection(
        string='status',
        selection=[
            ('new', "New"),
            ('scheduled', "Scheduled"),
            ('done', "Done"),
            ('cancelled', "Cancelled"),
        ],
        default='new',
    )

    @api.constrains('date')
    def _compute_date_clash(self):
        for rec in self:
            if rec.date < fields.Date.today():
                raise ValidationError('The visit date cannot be in the past.')
            if rec.date:
                rec.state = 'scheduled'
