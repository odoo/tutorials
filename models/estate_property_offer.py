from datetime import timedelta

from odoo import api, fields, models


class Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Ofertas'

    # Atributos

    price = fields.Float('Precio')
    status = fields.Selection(string='Estado',
                              selection=[('accepted', 'Acepada'),
                                         ('refused', 'Rechazada')], readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required='True')
    property_id = fields.Many2one('estate.propiedad', string='ID Propiedad', required=True)
    validity = fields.Integer(string='Validez (días)', default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_validity", string="Fecha límite")

    @api.depends('date_deadline')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            days = record.date_deadline - record.create_date.date()
            record.validity = days.days
