import { Component, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";

import { DashboardItem } from "./dashboard_item/dashboard_item";
import { ConfigDialog } from "./config_dialog/config_dialog";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout };

    setup() {
        this.action_service = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.dialog_service = useService("dialog");

        this.items = useState(registry.category("awesome_dashboard").getAll());
        let hidden_item_ids = browser.localStorage.getItem("hidden_item_ids").split(",");
        this.items.forEach(item => Object.assign(item, { visible: !hidden_item_ids.includes(item.id) }));
    }

    openPartnerKanbanView() {
        this.action_service.doAction("base.action_partner_form");
    }

    openCrmLeads() {
        this.action_service.doAction({
            type: 'ir.actions.act_window',
            name: 'CRM leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    openDashboardSettings() {
        this.dialog_service.add(ConfigDialog, { items: this.items });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
