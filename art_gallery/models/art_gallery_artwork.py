from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


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

    status = fields.Selection(
        string='Status',
        selection=[('available', 'Available'), ('reserved', 'Reserved'), ('sold', 'Sold')],
        required=True,
        default='available',
        copy=False,
    )

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

    def action_reserve(self):
        for record in self:
            if record.status == "sold":
                raise UserError("You cannot reserve a sold artwork")
            record.status = "reserved"
        return True

    def action_sell(self):
        for record in self:
            record.status = "sold"
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_sold(self):
        if any(record.status == "sold" for record in self):
            raise UserError(self.env._("You cannot delete a sold artwork"))
