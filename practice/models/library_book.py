from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError

class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author")
    published_date = fields.Date(string="Published Date")
    price = fields.Float(string="Price")
    author_id = fields.Many2one('library.author', string="Author ID")
    reader_ids = fields.Many2many('library.reader','book_ids', string="Reader ID")

    # Example ORM Functions
    @api.model
    def create(self, vals):
        """Override create method"""
        vals['name'] = vals.get('name', '').title()
        return super(Book, self).create(vals)

    def write(self, vals):
        """Override write method"""
        if 'price' in vals and vals['price'] < 0:
            raise ValidationError("Price cannot be negative!")
        return super(Book, self).write(vals)

    def unlink(self):
        """Override unlink method"""
        for book in self:
            if book.price > 100:
                raise ValidationError("Cannot delete books priced over 100!")
        return super(Book, self).unlink()
 
    def action_with_ORM_functions(self):
        # Create a new book record
        book = self.create({'name': 'Odoo Development', 'author': 'John Doe', 'price': 50})
        print(f"Created book: {book.name}")

        # Update the created book's price
        book.write({'price': 60})
        print(f"Updated book price to: {book.price}")

         # Search for books by author
        books = self.search([('author', '=', 'John Doe')])
        print(f"Found {len(books)} book(s) by John Doe.")

        # Browse a specific book by ID (assuming we know the ID, for example, 1)
        if books:
            book_to_browse = self.browse(1)
            print(f"Browsing book with ID {book_to_browse.id}: {book_to_browse.name}")

        # Delete the book record
        book_to_browse = self.browse(1)
        book_to_browse.unlink()
        print("Book deleted")

    def action_with_command(self):
        # Create example
        book1 = self.create({'name': 'Odoo Development with ravi', 
                             'author': 'John Doe', 
                             'price': 50,
                             'reader_ids': [Command.create({'name':'Ravi'})]})
         # link example
        readerKavi = self.env['library.reader'].create({'name': 'Kavi'})
        book2 = self.create({'name': 'Odoo Development with Kavi', 
                             'author': 'John Doe', 
                             'price': 50,
                             'reader_ids': [Command.link(readerKavi.id)]})
        # unlink example
        readerMavi = self.env['library.reader'].create({'name': 'Mavi'})
        book3 = self.create({'name': 'Odoo Development with mavi', 
                             'author': 'John Doe', 
                             'price': 50,
                             'reader_ids': [Command.link(readerMavi.id)]})
        book3.write({'reader_ids': [Command.unlink(readerMavi.id)]})
        
        # delete example
        readerSavi = self.env['library.reader'].create({'name': 'Savi'})
        book4 = self.create({'name': 'Odoo Development with Savi', 
                             'author': 'John Doe', 
                             'price': 50,
                             'reader_ids': [Command.link(readerSavi.id)]})
        book4.write({'reader_ids': [Command.delete(readerSavi.id)]})

        # clear example
        reader1 = self.env['library.reader'].create({'name': 'Reader 1'})
        reader2 = self.env['library.reader'].create({'name': 'Reader 2'})
        book5 = self.env['library.book'].create({
            'name': 'Book with Readers',
            'reader_ids': [Command.link(reader1.id), Command.link(reader2.id)],
        })

        book5.write({'reader_ids': [Command.clear()]})
