from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    property_sale_mode = fields.Selection(related="property_id.sale_mode")
