from odoo import fields, models


class Propiedad(models.Model):
    _name = 'estate_propiedad'
    _description = 'Propiedades Inmobiliaria'

    nombre = fields.Char('Nombre', required=True)
    descripcion = fields.Text('Descripción')
    cp = fields.Char('Código postal')
    fecha_disponibilidad = fields.Date('Fechad de disponibilidad', copy=False, default=3)    
    precio_esperado = fields.Float('Pricio esperado', required=True)
    precio_venta = fields.Float('Precio de venta', readonly=True, copy=False)
    dormitorios = fields.Integer('Dormitorios', default=2)
    area_habitable = fields.Integer('Área habitable')
    fachadas = fields.Integer('Fachadas')
    garaje = fields.Boolean('Garaje')
    jarin = fields.Boolean('Jardín')
    area_jardom = fields.Integer('Área de jardín')
    activo = fields.Boolean(default=True)

    #Estas dos lineas dan problemas
    orientation_jardin = fields.Selection(
        string='orientacion',
        selection=[('norte', 'Norte'), ('sur', 'Sur'), ('este','Este'), ('oeste','Oeste')])
    
    estado = fields.Selection(string='estado',
                               selection=[('nueva', 'Nueva'), 
                                ('oferta_recibida', 'Oferta recibida'),
                                ('vendida', 'vendida'),
                                ('oferta_aceptada', 'Oferta Aceptada'),
                                ('cancelada', 'Cancelada'),], 
                                required=True, 
                                copy=False, 
                                default="nueva")
    