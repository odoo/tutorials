# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Stage(models.Model):
    _inherit = "crm.stage"

    sequence_no = fields.Integer(string="Sequence No", copy=False)

    _sql_constraints = [("sequence_no_uniq", "unique(sequence_no)", "The 'Sequence No' must be unique.")]
