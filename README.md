# Odoo tutorials

This repository hosts the code for the bases of the modules used in the
[official Odoo tutorials](https://www.odoo.com/documentation/latest/developer/tutorials.html).

It has 3 branches for each Odoo version: one for the bases, one for the
[Discover the JS framework](https://www.odoo.com/documentation/latest/developer/tutorials/discover_js_framework.html)
tutorial's solutions, and one for the
[Master the Odoo web framework](https://www.odoo.com/documentation/latest/developer/tutorials/master_odoo_web_framework.html)
tutorial's solutions. For example, `17.0`, `17.0-discover-js-framework-solutions` and
`17.0-master-odoo-web-framework-solutions`.





###  architecture verview

- Odoo modules
Both server and client extensions are packaged as modules which are optionally loaded in a database. A module is a collection of functions and data that target a single purpose.

- Composition of a module
An Odoo module can contain a number of elements:
    - Business objects : A business object (e.g. an invoice) is declared as a Python class. The fields defined in these classes are automatically mapped to database columns thanks to the ORM layer.

    - ORM API
        Object Relational Mapping module:
        Hierarchical structure

        Constraints consistency and validation

        Object metadata depends on its status

        Optimised processing by complex query (multiple actions at once)

        Default field values

        Permissions optimisation

        Persistent object: DB postgresql

        Data conversion

        Multi-level caching system

        Two different inheritance mechanisms

        Rich set of field types:
        classical (varchar, integer, boolean, …)

        relational (one2many, many2one, many2many)

        functional

Object views
Define UI display

Data files
XML or CSV files declaring the model data:

views or reports,

configuration data (modules parametrization, security rules),

demonstration data

and more

Web controllers
Handle requests from web browsers

Static web data
Images, CSS or JavaScript files used by the web interface or website

None of these elements are mandatory. Some modules may only add data files (e.g. country-specific accounting configuration), while others may only add business objects. During this training, we will create business objects, object views and data files.

