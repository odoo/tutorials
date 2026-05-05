import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { DashboardConfiguration } from "./dashboard_configuration/dashboard_configuration";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem};

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics").loadStatistics);
        this.dialogService = useService("dialog");
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: localStorage.getItem("awesome_dashboard_disabled")?.split(',') || []
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window', target: 'current', res_model: 'crm.lead', views: [[false, "list"], [false, 'form'],],
        });
    }

    updateDashboard(disabledItems) {
        this.state.disabledItems = disabledItems;
    }

    openDialog() {
        this.dialog = this.dialogService.add(
            DashboardConfiguration,
            {items: this.items, disabledItems: this.state.disabledItems, doneUpdating: this.updateDashboard.bind(this)},
            {});
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
