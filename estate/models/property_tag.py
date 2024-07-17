from odoo import models, fields


class EstateTagsModel(models.Model):
    _name = "estate.tag"
    _description = "Real estate tags model"
    _order = 'tag'

    tag = fields.Char()
    color = fields.Char()

    _sql_constraints = [
        ('unique_tag', 'UNIQUE(tag)',
         'Expected tag to be unique'),
    ]
