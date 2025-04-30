import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Card } from "./card/card"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, Card };

    setup() {
        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.stats = useService("awesome_dashboard.statistics");
        this.avg_quantity = useState({ value: 0 });
        this.avg_time = useState({ value: 0 });
        this.nb_cancelled_orders = useState({ value: 0 });
        this.nb_new_orders = useState({ value: 0 });
        this.total_amount = useState({ value: 0 });

        onWillStart(async () => {
           const result = await this.stats.loadStatistics();
           this.avg_quantity.value = result.average_quantity
           this.avg_time.value = result.average_time;
           this.nb_cancelled_orders.value = result.nb_cancelled_orders;
           this.nb_new_orders.value = result.nb_new_orders;
           this.total_amount.value = result.total_amount;
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"],[false, "form"]],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
