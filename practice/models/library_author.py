from odoo import models, fields
from odoo import Command

class Author(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(string="Author Name")
    book_ids=fields.One2many('library.book','author_id')
