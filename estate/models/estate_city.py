from odoo import fields, models


class EstateCity(models.Model):
    _inherit = "res.city"

    estate_ids = fields.One2many("estate.property", inverse_name="city_id")
