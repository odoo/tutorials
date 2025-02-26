
import { LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState, xml } from "@odoo/owl";

export class AwesomeDashboardLoader extends Component {
    static components = { LazyComponent };
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'awesome_dashboard.dashboard'" />
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);
