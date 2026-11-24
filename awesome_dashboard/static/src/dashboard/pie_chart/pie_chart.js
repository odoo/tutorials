import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
        label: String,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.action = useService("action");
        this.chart = null;

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        useEffect(() => {
            this.renderChart();
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    onPieClick(ev, elements) { 
        if (!elements.length) {
            return;
        }
        const index = elements[0].index;
        const size = Object.keys(this.props.data)[index];

        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Orders with size %s", size),
            res_model: "crm.lead", 
            domain: [["name", "ilike", size]],
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const colors = labels.map((_, index) => getColor(index));

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: colors,
                    },
                ],
            },
            options: {
                onClick: this.onPieClick.bind(this),
            },
        });
    }
}
