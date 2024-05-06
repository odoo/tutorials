from odoo import fields, models


class property(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    nombre = fields.Char('name', required=True)
    descripcion = fields.Text("description")
    cp = fields.Char("Postal code")
    fecha_disponibilidad = fields.Date("Date availability", copy=False, default=3)    
    precio_esperado = fields.Float("Expected price", required=True)
    precio_vemta = fields.Float("Selling price", readonly=True, copy=False)
    dormitorios = fields.Integer("Bedrooms", default=2)
    area_habitable = fields.Integer("Living area")
    fachadas = fields.Integer("Facades")
    garaje = fields.Boolean("Garage")
    jarin = fields.Boolean("Garden")
    area_jardom = fields.Integer("Garden area")
    orientation_jardin = fields.Selection(string='Type',
                                          selection=[("North"), ('South'), ("East"), ("West")])
    activo = fields.Boolean(default=True)
    estado = fields.Selection(string='Type', selection=[("New"), ('Offer Received'), ("Sold"), ("Offer Accepted"), ("Cancelled"),]
                              , required=True, copy=False, default="New")
