from odoo import fields, models


class ArtGalleryArtwork(models.Model):
    _name = "art.gallery.artwork"
    _description = "Artwork exhibited or sold by the gallery"
    _order = "name asc"

    name = fields.Char(string="Title", required=True)
    artist = fields.Char()
    year = fields.Integer()
    description = fields.Text()
    image = fields.Image(max_width=1024, max_height=1024)
    price = fields.Float()
