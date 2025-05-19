/** @odoo-module **/

import { Component, onWillStart, useState, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { LazyComponent } from "@web/core/assets";

class DashboardAction extends Component {
    static template = xml`
    <LazyComponent bundle="'example_module.example_assets'" Component="'AwesomeDashboard'" />
`;
    static components = { LazyComponent };
}

registry.category("actions").add("awesome_dashboard.dashboard", DashboardAction);
