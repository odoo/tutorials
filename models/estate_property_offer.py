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
    date_deadline = fields.Date(compute="_compute_date_deadline", string="Fecha límite")
    creation_date = fields.Date(compute="_compute_create_date")
    validity = fields.Integer('Validez', default=7)

    @api.depends('creation_date')
    def _compute_create_date(self):
        for record in self:
            record.creation_date = record.create_date

    @api.depends('date_deadline')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.creation_date + timedelta(days=record.validity)
