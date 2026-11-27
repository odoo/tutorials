from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_artist = fields.Boolean()
    artwork_ids = fields.One2many("art.gallery.artwork", "artist_id")
