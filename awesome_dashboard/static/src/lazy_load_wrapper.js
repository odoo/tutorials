/** @odoo-module **/

import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { xml, Component } from "@odoo/owl";

class DashoboardLazyLoader extends Component {
  static components = { LazyComponent };
  static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'AwesomeDashboard'" />
    `;
}

registry
  .category("actions")
  .add("awesome_dashboard.dashboard", DashoboardLazyLoader);
