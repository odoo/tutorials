/** @odoo-module **/

import { Component } from "@odoo/owl";
import { PieChart } from "../piechart/piechart";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };

    static props = {
        title: { type: String },
        data: { type: Object }
    }

    setup() {
        this.action = useService("action");
    }

    _t(...args) {
        return _t(...args);
    }
}
