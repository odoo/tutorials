from odoo import fields, models, api


class Property(models.Model):
    _name = 'estate.propiedad'
    _description = 'Propiedades Inmobiliaria'

    # Atributos

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

    # Selecciones

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

    # Tipos Many2one

    property_type_id = fields.Many2one('estate.property.type', string='Tipo')
    seller_id = fields.Many2one("res.users", string="Vendedor", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Comprador", readonly=True)

    # Tags many2many

    tags_id = fields.Many2many('estate.property.tag', string='Etiqueta')

    # Ofertas

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Oferta')

    # Atributos calculados

    total_area = fields.Float(compute="_compute_total", string="Área total")

    @api.depends('area_habitable', 'area_jardin')
    def _compute_total(self):
        for record in self:
            record.total_area = record.area_habitable + record.area_jardin

    # Calculos con atributos relacionados

    best_offer = fields.Float(compute="_compute_best_offer", string="Mejor oferta", default="0.0")

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        offers = []
        for record in self:
            offers.append(record.offer_ids.price)
            best_offer = max(offers)

