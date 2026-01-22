import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";

import { DashboardItem } from "./dashboard_item/dashboard_item";
import { items } from "./dashboard_items";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout };

    setup() {
        this.action_service = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = items;
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
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
