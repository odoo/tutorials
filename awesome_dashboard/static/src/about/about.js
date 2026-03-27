import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";

class AwesomeAbout extends Component {
    static template = "awesome_dashboard.AwesomeAbout";
    static components = { Layout };
}

registry.category("actions").add("awesome_dashboard.about", AwesomeAbout);
