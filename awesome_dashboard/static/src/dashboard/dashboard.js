import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./components/dashboard_item/dashboard_item";

import { ControlPanelButtons } from "./components/control_panel_buttons/control_panel_buttons";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, ControlPanelButtons };
    static props = {};

    setup() {
        const svc = useService("awesome_dashboard.statistics");
        this.statistics = useState(svc.statistics);

        const removedIds = JSON.parse(
            localStorage.getItem("dashboard_config") || "[]"
        );

        this.items = registry
            .category("awesome_dashboard")
            .getAll()

        this.itemsondashboard = registry
            .category("awesome_dashboard")
            .getAll()
            .filter(item => !removedIds.includes(item.id));
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);