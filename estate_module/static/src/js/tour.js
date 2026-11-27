import { registry } from "@web/core/registry";


registry.category("web_tour.tours").add('estate_tour', {
    url: "/odoo",
    steps: () => [{
        trigger: '.o_app[data-menu-xmlid="estate_module.estate_menu_root"]',
        content: 'Start selling your properties from this app!',
        run: "click",
    }],
});
