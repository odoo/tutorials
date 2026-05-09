import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./item/dashboardItem";
import { PiChart } from "./chart/piChart";
import { NumberCard } from "./components/number_card";
import { PieChartCard } from "./components/pie_chart_card";
import { items } from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PiChart, NumberCard, PieChartCard }

    setup(){
        this.items = items
        this.display = {
            controlPanel: {}
        }
    this.action = useService("action")
    this.statistics = useState(useService("awesome_dashboard.statistics_service"))
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form")
    }

    openLeads(){
            this.action.doAction({
                type: 'ir.actions.act_window',
                name: 'crm leads',
                res_model: 'crm.lead',
                views: [[false,'list'], [false,'form']],
                target: 'current',
            })
        }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
