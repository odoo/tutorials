#self.env(environment())
        import ipdb; ipdb.set_trace()
open odoo in shell mode: odoo-bin shell

            #filtered: return the records in self(input recordset) satisfying param func
            #return self.browse([rec.id for rec in self if func(rec)])
            #self = recordset so here it is the offer_ids of property
            #for each record if func is true then we put its id in a list
            #browse() fetch a new recordset based on the id of the input list
            #other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id)

            #TODO: investigate the write method to update a recordset instead of a for loop
            #in fields.py def write(self, records, value):


python monkey patching: dynamically modify of extend method or class. Allows to change or replace methods attributes or classe (often used in testing)
[expression for item in iterable if condition]

run odoo server
./odoo-bin --addons-path="addons/,../enterprise/,../tutorials" -d db -u estate


server location: http://localhost:8069/
