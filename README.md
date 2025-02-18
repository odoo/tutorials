# Odoo tutorials

This repository hosts the code for the bases of the modules used in the
[official Odoo tutorials](https://www.odoo.com/documentation/latest/developer/tutorials.html).

It has 3 branches for each Odoo version: one for the bases, one for the
[Discover the JS framework](https://www.odoo.com/documentation/latest/developer/tutorials/discover_js_framework.html)
tutorial's solutions, and one for the
[Master the Odoo web framework](https://www.odoo.com/documentation/latest/developer/tutorials/master_odoo_web_framework.html)
tutorial's solutions. For example, `17.0`, `17.0-discover-js-framework-solutions` and
`17.0-master-odoo-web-framework-solutions`.



access_real_estate_property,Access for Users,model_estate_property,base.group_user,1,1,1,1
access_estate_property_type,access_estate_property_type,model_estate_property_type,,1,1,1,1
access_estate_property_tag,access_estate_property_tag,model_estate_property_tag,,1,1,1,1
access_estate_property_offer,access_estate_property_offer,model_estate_property_offer,,1,1,1,1


access_estate_property_type_manager,access.estate.property.type.manager,model_estate_property_type,estate_group_manager,1,1,1,1
access_estate_property_tags_manager,access.estate.property.tags.manager,model_estate_property_tags,estate_group_manager,1,1,1,1
access_estate_property_offer_manager,access.estate.property.offer.manager,model_estate_property_offer,estate_group_manager,1,1,1,1
access_estate_property_type_agent,access.estate.property.type.agent,model_estate_property_type,estate_group_user,1,0,0,0
access_estate_property_tags_agent,access.estate.property.tags.agent,model_estate_property_tags,estate_group_user,1,0,0,0
access_estate_property_agent,access.estate.property.agent,model_estate_property,estate_group_user,1,1,1,0
access_estate_property_offer_agent,access.estate.property.offer.agent,model_estate_property_offer,estate_group_user,1,1,1,0