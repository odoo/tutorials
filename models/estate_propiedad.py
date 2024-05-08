from odoo import fields, models


class Propiedad(models.Model):
    _name = 'estate.propiedad'
    _description = 'Propiedades Inmobiliaria'

    nombre = fields.Char('Nombre', required=True)
    descripcion = fields.Text('Descripción')
    cp = fields.Char('Código postal')
    fecha_disponibilidad = fields.Date('Fecha de disponibilidad', copy=False)
    precio_esperado = fields.Float('Precio esperado', required=True)
    precio_venta = fields.Float('Precio de venta', readonly=True, copy=False)
    dormitorios = fields.Integer('Dormitorios', default=2)
    area_habitable = fields.Integer('Área habitable')
    fachadas = fields.Integer('Fachadas')
    garaje = fields.Boolean('Garaje')
    jardin = fields.Boolean('Jardín')
    area_jardin = fields.Integer('Área de jardín')
    activo = fields.Boolean(default=True)

    orientacion_jardin = fields.Selection(string='Orientación',
                                          selection=[('norte', 'Norte'), ('sur', 'Sur'), ('este', 'Este'),
                                                     ('oeste', 'Oeste')])

    estado = fields.Selection(string='estado',
                              selection=[('nueva', 'Nueva'),
                                         ('oferta_recibida', 'Oferta recibida'),
                                         ('vendida', 'vendida'),
                                         ('oferta_aceptada', 'Oferta Aceptada'),
                                         ('cancelada', 'Cancelada'), ],
                              required=True,
                              copy=False,
                              default="nueva")
