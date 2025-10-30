/** @odoo-module **/
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from '@web/search/layout'
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart }

    setup() {
        this.action = useService("action");
        this.items = registry.category("awesome_dashboard").getAll()
        this.stats = useState(useService("statistics"));
        this.enabled = useState(this.getEnabledItems());
        this.state = useState({change: 0})
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeadView() {
        this.action.doAction({
            type: "ir.actions.act_window",
            mane: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    apply() {
        this.items.forEach(item => {
            const el = document.getElementById(`checkbox-${item.id}`)
            localStorage.setItem(item.id, el.checked);
        })
        this.enabled = this.getEnabledItems();
        this.state.change++; // Force rerender because the line above doesn't do it
        console.log(this.enabled)
    }

    getEnabledItems() {
        return this.items.filter(item => localStorage.getItem(item.id) === 'true').map(x => x.id)
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
