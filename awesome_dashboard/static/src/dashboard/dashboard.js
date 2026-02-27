import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks"; 
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./components/dashboard_item/dashboard_item";
import { PieChart } from "./components/pie_chart/pie_chart";
import { NumberCard } from "./components/number_card/number_card";
import { PieChartCard } from "./components/pie_chart_card/pie_chart_card";
import { browser } from "@web/core/browser/browser";
import { FilterDialogue } from "./components/filter_dialog/filter_dialog";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart, NumberCard, PieChartCard };

    setup() {
        this.items = registry.category("awesome_dashboard").getAll();
        this.action = useService("action");
        const statisticsService = useService("statistics");
        this.statistics = useState(statisticsService.statistics);
        this.dialog = useService("dialog");
        this.state = useState({
            disabledItems: JSON.parse(browser.localStorage.getItem("disabledDashboardItems") || "[]"),
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads(e) {
        this.action.doAction({
            type: 'ir.actions.act_window', // The Action we will do
            name: _t('Leads'), // The name that will be in the breadcrumb
            res_model: 'crm.lead', // The model that we will open the view of
            views: [[false, 'list'], [false, 'form']], // [choose if their is a specific view id we want to choose, the type of view we are choosing]
            search_view_id: [false],  // chooses the search view we want to use.
        });
    }

    openFilterDialog() {
        this.dialog.add(FilterDialogue, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdate: (disabledIds) => {
                this.state.disabledItems = disabledIds;
            },
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
