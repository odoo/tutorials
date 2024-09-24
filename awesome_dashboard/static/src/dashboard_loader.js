/** @odoo-module **/

import {registry} from "@web/core/registry";
import {Component, xml} from "@odoo/owl";
import {LazyComponent} from "@web/core/assets";

export class DashboardLoader extends Component {
    static components = {LazyComponent}
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'awesome_dashboard'" props="props"/>
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", DashboardLoader);