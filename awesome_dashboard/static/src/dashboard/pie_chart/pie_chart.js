/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted, onWillUnmount, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: { type: Object },
        onClick: { type: Function, optional: true },
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            const config = {
                type: "pie",
                data: {
                    labels: Object.keys(this.props.data),
                    datasets: [
                        {
                            label: "Orders by Size",
                            data: Object.values(this.props.data),
                            backgroundColor: [
                                "red",
                                "blue",
                                "yellow",
                                "green",
                                "purple",
                            ],
                        },
                    ],
                },
                options: {
                    onClick: (e, items) => {
                        if (items.length > 0 && this.props.onClick) {
                            const index = items[0].index;
                            const label = this.chart.data.labels[index];
                            this.props.onClick(label);
                        }
                    },
                },
            };
            this.chart = new window.Chart(this.canvasRef.el, config);
        });

        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this.chart.data.labels = Object.keys(nextProps.data);
                this.chart.data.datasets[0].data = Object.values(nextProps.data);
                this.chart.update();
            }
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }
}
