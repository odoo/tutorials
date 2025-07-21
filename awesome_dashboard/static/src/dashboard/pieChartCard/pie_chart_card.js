import { Component } from "@odoo/owl";
import { PieChart } from "@awesome_dashboard/dashboard/pieChart/piechart";
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

    get translatedTitle() {
        return _t(this.props.title);
    }

    get translatedValue() {
        return _t(this.props.value);
    }
}
