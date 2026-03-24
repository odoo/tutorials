import {Component, onMounted, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {useService} from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";
import {DashboardItem} from "./components/dashboard_item/dashboard_item";
import {PieChart} from "./components/pie_chart/pie_chart";
import {NumberCard} from "./components/number_card/number_card";
import {PieChartCard} from "./components/pie_chart_card/pie_chart_card";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {
        Layout,
        DashboardItem,
        PieChart,
    };

    setup() {
        this.action = useService("action");
        this.orm = useService("orm");

        this.statistics = useState(useService("statistics"));

        this.state = useState({
            items: null,
        });

        onMounted(async () => {
            await this._refreshSources();
        })
    }

    openCustomerKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Pipeline"),
            target: "current",
            res_model: "crm.lead",
            views: [[false, "kanban"], [false, "list"], [false, "form"]],
        });
    }

    openConfiguration() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Dashboard Configuration"),
            target: "current",
            res_model: "awesome_dashboard.dashboard.item",
            views: [[false, "list"], [false, "form"]],
            context: {
                search_default_my_items: true,
            },
        });
    }

    async _refreshSources() {
        const results = await this.orm.call("awesome_dashboard.dashboard.item", "get_by_current_user");

        const items = [];

        for (const result of results) {
            const item = {
                id: result.id,
                description: result.name,
                size: result.size,
            }

            switch (result.component_type) {
                case 'number_card':
                    item.component = NumberCard;
                    item.props = (data) => ({
                        title: result.description,
                        value: data[result.property],
                    });
                    break;
                case 'pie_chart_chart':
                    item.component = PieChartCard;
                    item.props = (data) => ({
                        title: result.description,
                        data: data[result.property],
                    });
                    break;
            }

            items.push(item);
        }

        this.state.items = items;
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
