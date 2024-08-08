[1mdiff --git a/estate/__manifest__.py b/estate/__manifest__.py[m
[1mindex 34f00b6cbd17..5043e3cdf2c8 100644[m
[1m--- a/estate/__manifest__.py[m
[1m+++ b/estate/__manifest__.py[m
[36m@@ -9,10 +9,10 @@[m
     'data': [[m
         'security/ir.model.access.csv',[m
         'views/estate_property_views.xml',[m
[31m-        'views/estate_menus.xml',[m
         'views/estate_property_type_view.xml',[m
         'views/estate_property_tag.xml',[m
[31m-        'views/estate_property_offer.xml'[m
[32m+[m[32m        'views/estate_property_offer.xml',[m
[32m+[m[32m        'views/estate_menus.xml'[m
     ],[m
     'installable': True,[m
     'application': True,[m
[1mdiff --git a/estate/models/estate_peoperty_offer.py b/estate/models/estate_peoperty_offer.py[m
[1mindex 0d69d5d23dce..7bf2e41233bc 100644[m
[1m--- a/estate/models/estate_peoperty_offer.py[m
[1m+++ b/estate/models/estate_peoperty_offer.py[m
[36m@@ -6,6 +6,7 @@[m [mfrom odoo.exceptions import UserError, ValidationError[m
 class EstatePropertyOffer(models.Model):[m
     _name = 'estate.property.offer'[m
     _description = 'Estate Property offer'[m
[32m+[m[32m    _order = 'price desc'[m
 [m
     price = fields.Float('Price')[m
     status = fields.Selection([[m
[1mdiff --git a/estate/models/estate_property.py b/estate/models/estate_property.py[m
[1mindex 2e146f7b988b..21d252a4717d 100644[m
[1m--- a/estate/models/estate_property.py[m
[1m+++ b/estate/models/estate_property.py[m
[36m@@ -7,8 +7,9 @@[m [mfrom odoo.tools.float_utils import float_compare[m
 class EstateProperty(models.Model):[m
     _name = "estate.property"[m
     _description = "Real Estate Property"[m
[32m+[m[32m    _order = 'id desc'[m
 [m
[31m-    name = fields.Char(required=True)[m
[32m+[m[32m    name = fields.Char('Title',required=True)[m
     description = fields.Text()[m
     postcode = fields.Char(string='Postcode')[m
     date_availability = fields.Date([m
[36m@@ -94,5 +95,7 @@[m [mclass EstateProperty(models.Model):[m
     def _check_selling_price(self):[m
         for record in self:[m
             if record.expected_price > 0:[m
[32m+[m[32m                print("befro exception raise selling price----",float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01))[m
                 if record.selling_price and float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01) < 0:[m
[32m+[m[32m                    print("after selling price----",float_compare(record.selling_price, record.expected_price * 0.9, precision_rounding=0.01))[m
                     raise ValidationError("The selling price must be at least 90% of the expected price.")[m
[1mdiff --git a/estate/models/estate_property_tag.py b/estate/models/estate_property_tag.py[m
[1mindex 99a03bfece71..5c1c357442be 100644[m
[1m--- a/estate/models/estate_property_tag.py[m
[1m+++ b/estate/models/estate_property_tag.py[m
[36m@@ -4,6 +4,7 @@[m [mfrom odoo import fields, models[m
 class EstatePropertyTag(models.Model):[m
     _name = 'estate.property.tag'[m
     _description = 'Estate Property tag'[m
[32m+[m[32m    _order = 'name'[m
 [m
     name = fields.Char(required=True)[m
 [m
[1mdiff --git a/estate/models/estate_property_type.py b/estate/models/estate_property_type.py[m
[1mindex b8d9db027b61..7613ae0eb729 100644[m
[1m--- a/estate/models/estate_property_type.py[m
[1m+++ b/estate/models/estate_property_type.py[m
[36m@@ -4,8 +4,11 @@[m [mfrom odoo import fields, models[m
 class EstatePropertyTypes(models.Model):[m
     _name = 'estate.property.type'[m
     _description = 'Estate Property Types'[m
[32m+[m[32m    _order = 'sequence, name asc'[m
 [m
[31m-    name = fields.Char(required=True)[m
[32m+[m[32m    name = fields.Char("Title",required=True)[m
[32m+[m[32m    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")[m
[32m+[m[32m    sequence = fields.Integer()[m
 [m
     _sql_constraints = [[m
         ('check_unique_name', 'UNIQUE(name)',[m
[1mdiff --git a/estate/views/estate_property_type_view.xml b/estate/views/estate_property_type_view.xml[m
[1mindex 989d7cfbe365..cbaa4904d6e8 100644[m
[1m--- a/estate/views/estate_property_type_view.xml[m
[1m+++ b/estate/views/estate_property_type_view.xml[m
[36m@@ -5,11 +5,20 @@[m
         <field name="model">estate.property.type</field>[m
         <field name="arch" type="xml">[m
             <form string="Types of Property">[m
[31m-                <sheet>[m
                     <h1>[m
                         <field name="name"/>[m
                     </h1>[m
[31m-                </sheet>[m
[32m+[m[32m                <notebook>[m
[32m+[m[32m                    <page string="Properties">[m
[32m+[m[32m                        <field name="property_ids">[m
[32m+[m[32m                            <tree string='Property'>[m
[32m+[m[32m                                <field name='name'/>[m
[32m+[m[32m                                <field name='expected_price'/>[m
[32m+[m[32m                                <field name='state'/>[m
[32m+[m[32m                            </tree>[m
[32m+[m[32m                        </field>[m
[32m+[m[32m                    </page>[m
[32m+[m[32m                </notebook>[m
             </form>[m
         </field>[m
     </record>[m
[36m@@ -19,6 +28,7 @@[m
         <field name="model">estate.property.type</field>[m
         <field name="arch" type="xml">[m
             <tree string="Types of Property">[m
[32m+[m[32m                <field name="sequence" widget="handle"/>[m
                 <field name="name"/>[m
             </tree>[m
         </field>[m
[1mdiff --git a/estate/views/estate_property_views.xml b/estate/views/estate_property_views.xml[m
[1mindex 23ad0cc297d0..b69271043955 100644[m
[1m--- a/estate/views/estate_property_views.xml[m
[1m+++ b/estate/views/estate_property_views.xml[m
[36m@@ -36,8 +36,9 @@[m
         <field name="arch" type="xml">[m
             <form string="Property">[m
                 <header>[m
[31m-                    <button name="action_set_sold" type="object" string="Sold"/>[m
[31m-                    <button name="action_set_canceled" type="object" string="Cancel"/>[m
[32m+[m[32m                    <button name="action_set_sold" type="object" string="Sold" invisible="state == 'sold' or state == 'canceled'"/>[m
[32m+[m[32m                    <button name="action_set_canceled" type="object" string="Cancel" invisible="state == 'sold' or state == 'canceled'"/>[m
[32m+[m[32m                    <field name="state" widget="statusbar"/>[m
                 </header>[m
                 <sheet>[m
                     <group>[m
[36m@@ -57,7 +58,7 @@[m
                             <field name="selling_price" />[m
                             <field name="best_price"/>[m
                         </group>[m
[31m-                        <notebook>[m
[32m+[m[32m                    <notebook>[m
                         <page string="Desciption">[m
                             <group>[m
                                 <field name="bedrooms" />[m
[36m@@ -71,12 +72,6 @@[m
                                 <field name="total_area"/>[m
                             </group>[m
                         </page>[m
[31m-                        <page string = "otherInfo">[m
[31m-                            <group>[m
[31m-                                <field name="buyer_id" />[m
[31m-                                <field name="sell_person_id" />[m
[31m-                            </group>[m
[31m-                        </page>[m
                         <page string="Offer">[m
                             <field name="offer_ids">[m
                                <tree>[m
[36m@@ -90,6 +85,12 @@[m
                                </tree>[m
                             </field>[m
                          </page>[m
[32m+[m[32m                         <page string = "otherInfo">[m
[32m+[m[32m                            <group>[m
[32m+[m[32m                                <field name="buyer_id" />[m
[32m+[m[32m                                <field name="sell_person_id" />[m
[32m+[m[32m                            </group>[m
[32m+[m[32m                        </page>[m
                     </notebook>[m
                 </sheet>[m
             </form>[m
