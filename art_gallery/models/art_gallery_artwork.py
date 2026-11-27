from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class ArtGalleryArtwork(models.Model):
    _name = "art.gallery.artwork"
    _description = "Artwork exhibited or sold by the gallery"
    _order = "name asc"

    name = fields.Char(string="Title", required=True)
    artist_id = fields.Many2one(
        "res.partner",
        string="Artist",
        domain=[('is_artist', '=', True)],
        context={'default_is_artist': True},
    )
    year = fields.Integer()
    age = fields.Integer(compute="_compute_age")
    description = fields.Text()
    image = fields.Image(max_width=1024, max_height=1024)
    price = fields.Float()
    commission_rate = fields.Integer(string="Commission (%)")
    artist_payout = fields.Float(compute="_compute_artist_payout")

    status = fields.Selection(
        string='Status',
        selection=[('available', 'Available'), ('reserved', 'Reserved'), ('sold', 'Sold')],
        required=True,
        default='available',
        copy=False,
    )

    exhibition_ids = fields.Many2many("art.gallery.exhibition", string="Exhibitions")

    _check_price = models.Constraint(
        'CHECK(price >= 0)',
        'The price must be positive.',
    )

    _check_unique_title = models.Constraint(
        'UNIQUE(name, artist_id)',
        'An artist cannot have 2 artworks with the same title.',
    )

    _check_commission_rate = models.Constraint(
        'CHECK(commission_rate BETWEEN 0 AND 100)',
        'The commission must be between 0 and 100%.',
    )

    @api.depends('year')
    def _compute_age(self):
        for record in self:
            record.age = fields.Date.today().year - record.year if record.year else 0

    @api.depends('price', 'commission_rate')
    def _compute_artist_payout(self):
        for record in self:
            record.artist_payout = record.price * (1 - record.commission_rate / 100)

    @api.constrains('year')
    def _check_year(self):
        current_year = fields.Date.today().year
        for artwork in self:
            if artwork.year > current_year:
                raise ValidationError(self.env._("The year cannot be in the future."))

    @api.constrains('exhibition_ids')
    def _check_exhibition_dates(self):
        self.exhibition_ids._check_dates_for_each_artwork()

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
