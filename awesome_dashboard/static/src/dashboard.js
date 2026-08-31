import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem";
import { rpc } from "@web/core/network/rpc";
import { PieChart } from "./pieChart";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.state = useState(useService("statistics"));
    }

    async openCustomers() {

        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'res.partner',
            views: [[false, 'kanban']],
        });
    }

    async openLeads() {

        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'kanban']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
