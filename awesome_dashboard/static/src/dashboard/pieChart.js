import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
        onSectionClick: { type: Function, optional: true },

    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        useEffect(
            () => {
                const keys = Object.keys(this.props.data);
                const chart = new Chart(this.canvasRef.el, {
                    type: "pie",
                    data: {
                        labels: keys.map((k) => k.toUpperCase()),
                        datasets: [{
                            data: Object.values(this.props.data),
                            backgroundColor: ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"],
                        }],
                    },
                    options: {
                        maintainAspectRatio: false,
                        plugins: { legend: { position: "bottom" } },
                        onClick: (event, elements) => {
                            if (elements.length) {
                                this.props.onSectionClick?.(keys[elements[0].index]);
                            }
                        },
                    },
                });
                return () => chart.destroy();
            },
            () => [this.props.data]
        );
    }
}
