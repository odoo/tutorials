# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

from random import randint


class EstateTagCategory(models.Model):
    _name = "estate.tag.category"
    _description = "Estate Tag Category"
    _order = "sequence"

    def _default_sequence(self):
        """
        Here we use a _default method instead of ordering on 'sequence, id' to
        prevent adding a new related stored field in the 'event.tag' model that
        would hold the category id.
        """
        return (self.search([], order="sequence desc", limit=1).sequence or 0) + 1

    name = fields.Char("Name", required=True, translate=True)
    sequence = fields.Integer('Sequence', default=_default_sequence)
    tag_ids = fields.Many2many("estate.tag", "category_id", string="Tags")


class EstateTag(models.Model):
    _name = "estate.tag"
    _description = "Estate Tag"
    _order = "category_sequence, sequence, id"

    def _default_color(self):
        return randint(1, 11)

    name = fields.Char("Name", required=True, translate=True)
    sequence = fields.Integer("Sequence", default=0)
    category_id = fields.Many2one("estate.tag.category", string="Category", index=True, ondelete='cascade')
    category_sequence = fields.Integer(related="category_id.sequence", string='Category Sequence', store=True)
    color = fields.Integer(
        string='Color Index', default=lambda self: self._default_color(),
        help='Tag color. No color means no display in kanban or front-end, to distinguish internal tags from public categorization tags.')

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The tag name has to be unique',
    )
