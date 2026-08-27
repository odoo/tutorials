import { Component, onWillStart, useState, onMounted } from "@odoo/owl";
import { Layout } from "@web/search/layout"
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboard_item";
import { rpc } from "@web/core/network/rpc";
import { Piechart } from "./piechart/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = {
        DashboardItem,
        Layout,
        Piechart
    }
    setup() {
        this.action = useService("action")
        this.caching = useService("myCaching")
        this.statistics = useState({})
        this.items = registry.category("awesome_dashboard").get("items");

        onWillStart(async () => {
            const stats = await this.caching.loadStatistics()
            Object.assign(this.statistics, await stats());
        })
        onMounted(() => {
            setInterval(async () => {
                console.log("in de functie")
                const stats = await this.caching.loadStatistics()
                console.log(await stats())
                Object.assign(this.statistics, await stats());
            }, 5000)
        })
    }

    kanban_action() {
        this.action.doAction("base.action_partner_form")
    }

    leads_action() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'crm action',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
