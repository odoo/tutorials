import {Component, useState} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {DashboardItem} from "./dashboard_item";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem};

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.state = useState({
            statistics: null,
        });

    }

    async willStart() {
        this.state.statistics = await this.statistics.loadStatistics();
    }


    openCustomers() {

        this.action.doAction("res.partner.action_partner_kanban");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "kanban"], [false, "form"]],
            target: "current",
        });
    }

    openCustomers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Customers",
            res_model: "res.partner",
            views: [[false, "kanban"], [false, "form"]],
            target: "current",
        });
    }

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
