from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ArtGalleryExhibition(models.Model):
    _name = "art.gallery.exhibition"
    _description = "Exhibition of artworks in the gallery"
    _order = "start_date desc"

    name = fields.Char(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    is_finished = fields.Boolean(compute="_compute_is_finished")

    artwork_ids = fields.Many2many("art.gallery.artwork", string="Artworks")

    @api.depends('end_date')
    def _compute_is_finished(self):
        today = fields.Date.today()
        for exhibition in self:
            exhibition.is_finished = bool(exhibition.end_date) and exhibition.end_date < today

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for exhibition in self:
            if exhibition.end_date < exhibition.start_date:
                raise ValidationError(self.env._("The exhibition cannot end before it starts."))

    @api.constrains('start_date', 'end_date', 'artwork_ids')
    def _check_dates_for_each_artwork(self):
        for exhibition in self:
            if not exhibition.artwork_ids:
                continue
            overlapping = self.search([
                ('id', '!=', exhibition.id),
                ('artwork_ids', 'in', exhibition.artwork_ids.ids),
                ('start_date', '<=', exhibition.end_date),
                ('end_date', '>=', exhibition.start_date),
            ])
            for other in overlapping:
                artworks = exhibition.artwork_ids & other.artwork_ids
                raise ValidationError(self.env._(
                    "%(artworks)s already in the exhibition %(exhibition)s on these dates.",
                    artworks=", ".join(artworks.mapped('name')),
                    exhibition=other.name,
                ))
