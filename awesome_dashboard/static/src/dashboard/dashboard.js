/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "@awesome_dashboard/dashboard/dashboard_item";
import { registry } from "@web/core/registry";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, AwesomeDashboardItem };

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard_statistics"));
        this.items = registry.category("awesome_dashboard").get("data");
    }

    onClickCustomers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Customers",
            target: "current",
            res_model: "res.partner",
            views: [[false, "kanban"]],
        });
    }

    onClickLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"]],
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
