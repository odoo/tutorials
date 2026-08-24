import { Component, xml, onMounted, onWillStart, onWillUnmount, useRef } from "@odoo/owl";

import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class PieChart extends Component {
    static props = {
        data: { type: Object },
    };

    static template = xml`
        <div class="w-50 mx-auto">
            <canvas t-ref="canvas"/>
        </div>
    `;

    setup() {
        this.canvasRef = useRef("canvas");
        this.action = useService("action");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        onMounted(() => {
            this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    labels: Object.keys(this.props.data),
                    datasets: [{ data: Object.values(this.props.data) }],
                },
                options: {
                    onClick: (ev, elements) => this.onClick(elements),
                },
            });
        });

        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    onClick([element]) {
        if (!element) {
            return;
        }
        const size = this.chart.data.labels[element.index];
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Orders of size %s", size),
            res_model: "sale.order",
            domain: [["size", "=", size]],
            views: [[false, "list"], [false, "form"]],
        });
    }
}
