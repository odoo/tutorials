from odoo import api, fields, models


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char('Title', required=True)
    author_name = fields.Char('Author')
    purchase_price = fields.Float('Purchase Price')
    selling_price = fields.Float('Selling Price')
    rent_price = fields.Float('Rent Price(per day)')
    quantity = fields.Integer('Quantity')

    book_tag_ids = fields.Many2many("library.book.tag", string="Tags")

    book_rent_ids = fields.One2many("library.book.rent", "book_id")
    borrower_count = fields.Integer('Borrower Count', compute='_compute_borrower_count')

    @api.depends('book_rent_ids')
    def _compute_borrower_count(self):
        for book in self:
            book.borrower_count = len(book.book_rent_ids)

    def action_open_rent_wizard(self):
        self.ensure_one()
        return {
            'name': "Rent",
            'type': 'ir.actions.act_window',
            'res_model': 'library.book.rent',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'current_book_id': self.id,
            },
        }
