import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";
    static props = {
        size: { type: Number, optional: true },
    };

    get width() {
        const size = this.props.size || 1;
        return `width: ${18 * size}rem;`;
    }
}
