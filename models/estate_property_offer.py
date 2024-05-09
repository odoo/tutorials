from odoo import fields, models


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
