import { Component, usePlugin, useProps, types as t } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { ActionPlugin } from "@web/webclient/actions/action_plugin";
import { PieChart } from "./pie_chart";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";
    static components = { PieChart };

    action = usePlugin(ActionPlugin);

    props = useProps({
        title: t.string(),
        values: t.object(),
    });

    openOrders(size) {
        // There is no real orders model in this tutorial: "sale.order" and its
        // "size" field are placeholders, to replace with the actual ones.
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Orders of size %s", size),
            res_model: "sale.order",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: [["size", "=", size]],
        });
    }
}
