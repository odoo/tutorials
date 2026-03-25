import { Component } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";

export class AboutPage extends Component {
    static template = "awesome_dashboard.AboutPage";
    static components = { Layout };
}

registry.category("lazy_components").add("AboutPage", AboutPage);
