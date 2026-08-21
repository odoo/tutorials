import { Component, xml, onWillStart } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

import { DashboardItem } from "./dashboard_item";
import { PieChart } from "../piechart/piechart";

class AwesomeDashboard extends Component {
    static template = xml`
        <div class="p-2 d-flex gap-2">
            <button t-on-click="gotoCustomers"  class="btn btn-primary">Customers</button>
            <button t-on-click="gotoLeads" class="btn btn-primary">Leads</button>
        </div>
        <Layout display="{ controlPanel: {} }" className="'o_dashboard h-100'">
            <t t-foreach="stats" t-as="s" t-key="s.key">
                <DashboardItem title="s.title" size="s.size">
                    <t t-esc="state[s.key]"/>
                </DashboardItem>
            </t>
            <DashboardItem title="'Shirt orders by size'" size="2">
                <PieChart data="state.orders_by_size"/>
            </DashboardItem>
        </Layout>
    `;

    static components = { Layout, DashboardItem, PieChart }

    setup() {
        this.action = useService("action")
        this.state = useService("awesome_dashboard.statistics")

        this.stats = [
            { title: "Average amount of t-shirt by order this month", key: "average_quantity", size: 1.5 },
            { title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'", key: "average_time", size: 2 },
            { title: "Number of new orders this month", key: "nb_new_orders", size: 1 },
            { title: "Number of cancelled orders this month", key: "nb_cancelled_orders", size: 1.5 },
            { title: "Total amount of new orders this month", key: "total_amount", size: 1.5 },
        ]
        
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js")
        })
    }

    gotoCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    gotoLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, 'list'], [false, 'form']],
        })
    }
    
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
