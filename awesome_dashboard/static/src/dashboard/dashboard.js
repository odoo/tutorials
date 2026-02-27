import { Component, onWillStart, useEffect, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboardItem";
import { PieChart } from "./pie_chart/pieChart"
import { DashboardDialog } from "./dashboard_dialog/dashboardDialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.items = registry.category("awesome_dashboard").getAll();
        this.hidden = useState({value: JSON.parse(localStorage.getItem("awesome_dashboard/hidden_items")) || []});

        this.action = useService("action");
        this.dialog = useService("dialog");
        const statistics = useService("statistics");

        const statisticsData = useState(statistics.data);


        const updateData = (async (loadStatistics) => {
            this.result = await loadStatistics()
        }).bind(this)

        onWillStart(async () => {
            await updateData(statisticsData.loadStatistics)
        })

        useEffect((loadStatistics) => {
            updateData(loadStatistics)
        }, () => [statisticsData.loadStatistics])
    }
    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads(){
        this.action.doAction({
            type: "ir.actions.act_window",
            views: [[false, "list"], [false, 'form']],
            res_model: "crm.lead",
        })
    }

    openDialog() {
        this.dialog.add(DashboardDialog, {
            hidden: this.hidden.value,
            save: ((hidden) => {
                this.hidden.value = hidden;
                localStorage.setItem("awesome_dashboard/hidden_items", JSON.stringify(hidden));
            }).bind(this)
        })
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
