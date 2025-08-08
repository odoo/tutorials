{
    "name": "warranty",
    "version" : "1.0",
    "category" : "Sales",
   
    "website": "https://www.odoo.com",
    "depends": ["base","sale_management","spreadsheet"],
    "data" : [
      "security/ir.model.access.csv",
      "wizard/product_warranty_wizard_views.xml",
      "views/product_templates_views.xml",
      "views/product_warranty_views.xml",
      "views/sale_order_views.xml",
      "views/product_warranty_menus.xml",
          ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}    