from odoo import models, fields

class LibraryBookTag(models.Model):
    _name = 'library.book.tag'
    _description = 'Library Book Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer()
