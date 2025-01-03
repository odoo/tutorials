from odoo import models, fields
from odoo import Command

class Reader(models.Model):
    _name = 'library.reader'
    _description = 'Reader'

    name = fields.Char(string="Reader Name")
    book_ids=fields.Many2many('library.book','reader_ids')
