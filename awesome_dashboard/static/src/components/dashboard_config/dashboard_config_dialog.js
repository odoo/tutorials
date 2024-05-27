/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { useDashboardConfig } from "../../hooks";

export class DashboardConfigDialog extends Component {
    static template = 'awesome_dashboard.dashboard_config_dialog';
    static components = { Dialog };

    setup() {
        this.dashboardConfig = useDashboardConfig();

        this.dashboardItems = registry.category("awesome_dashboard").getAll();

        this.env.dialogData.close = () => this.close();
    }

    updateItem(event) {
        const id = event.target.name;
        const isVisible = event.target.checked;
        this.dashboardConfig.setItem(id, isVisible);
    }

    async close() {
        await this.dashboardConfig.save();
        this.props.close();
    }
}
