from odoo import api, models, fields
from odoo.exceptions import ValidationError


class LibraryBookRent(models.Model):
    _name = 'library.book.rent'
    _description = 'Library Book Rent'

    book_id = fields.Many2one('library.book', string='Book', required=True)
    customer_id = fields.Many2one("res.partner", required=True)
    rent_duration = fields.Integer('Rent Duration(per day)')
    rent_start_date = fields.Date('Rent Start Date', default=fields.Date.today())
    rent_end_date = fields.Date('Rent End Date', compute="_compute_rent_end_date")
    total_rent = fields.Float('Total Rent', compute='_compute_total_rent')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        current_book_id = self.env.context.get('current_book_id')
        book_id = self.env["library.book"].browse(current_book_id)

        res.update({
            'book_id': book_id.id,
        })
        return res

    @api.depends('rent_start_date', 'rent_duration')
    def _compute_rent_end_date(self):
        for book in self:
            if book.rent_start_date and book.rent_duration:
                book.rent_end_date = fields.Date.add(book.rent_start_date, days=book.rent_duration)
            else:
                book.rent_end_date = False

    @api.depends('rent_duration', 'book_id.rent_price')
    def _compute_total_rent(self):
        for book in self:
            book.total_rent = book.rent_duration * book.book_id.rent_price

    @api.constrains('rent_duration')
    def _check_rent_duration(self):
        for book in self:
            if book.rent_duration > 15:
                raise ValidationError('Rent Duration must be less than 15 days')

    @api.constrains('customer_id')
    def _check_customer_id(self):
        for book in self:
            if not book.customer_id.is_library_member:
                raise ValidationError('Customer must be a library member')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.book_id and record.book_id.quantity:
                record.book_id.quantity -= 1
            else:
                raise ValidationError('Uh oh!! Book is out of stock.')
        return records
