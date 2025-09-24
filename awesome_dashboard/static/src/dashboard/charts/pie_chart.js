/** @odoo-module **/

import { Component, onMounted, onWillStart, onWillUnmount, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = { data: Object, onSliceClick: { type: Function, optional: true } };

    setup() {
        const ref = this.canvasRef = useRef("canvas");
        let chart, handler;

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        onMounted(() => {
            const entries = Object.entries(this.props.data);
            chart = new window.Chart(ref.el.getContext("2d"), {
                type: "pie",
                data: {
                    labels: entries.map(([k]) => k),
                    datasets: [{ data: entries.map(([, v]) => v), backgroundColor: ["red", "green", "blue"] }]
                }
            });

            handler = e => {
                const a = chart.getElementAtEvent?.(e) || chart.getElementsAtEventForMode?.(e, "nearest", { intersect: true }, true);
                if (a?.length) this.props.onSliceClick?.(chart.data.labels[a[0]._index ?? a[0].index], a[0]._index ?? a[0].index);
            };
            ref.el.addEventListener("click", handler);
        });

        onWillUnmount(() => ref.el?.removeEventListener("click", handler));
    }
}
