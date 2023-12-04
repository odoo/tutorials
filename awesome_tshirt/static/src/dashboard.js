/** @odoo-module **/

import { Component, useSubEnv } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { getDefaultConfig } from "@web/views/view";
import { Layout } from "@web/search/layout";

class AwesomeDashboard extends Component {
    setup() {
        const config = {
            ...getDefaultConfig(),
            ...this.env.config,
        };
        useSubEnv({ config });
    }
}

AwesomeDashboard.components = { Layout };
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
