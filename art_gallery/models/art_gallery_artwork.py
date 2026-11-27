from odoo import api, fields, models
from odoo.exceptions import ValidationError


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

    _check_price = models.Constraint(
        'CHECK(price >= 0)',
        'The price must be positive.',
    )

    _check_unique_title = models.Constraint(
        'UNIQUE(name, artist)',
        'An artist cannot have 2 artworks with the same title.',
    )

    @api.constrains('year')
    def _check_year(self):
        current_year = fields.Date.today().year
        for artwork in self:
            if artwork.year > current_year:
                raise ValidationError(self.env._("The year cannot be in the future."))
