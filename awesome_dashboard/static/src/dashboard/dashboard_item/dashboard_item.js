/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { NumberCard } from "../number_card/number_card";
import { PieChartCard } from "../pie_chart_card/pie_chart_card";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static components = { NumberCard, PieChartCard };
    static props = {
        size: {
            type: Number,
            optional: true,
        },
        stat: {
            type: Number,
            optional: true,
        },
    };
    static defaultProps = {
        size: 1,
    };
}

registry.category("main.components").add("awesome_dashboard.dashboard_item", DashboardItem);
