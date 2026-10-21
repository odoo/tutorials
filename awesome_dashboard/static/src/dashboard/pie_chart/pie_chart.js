import { loadJS } from "@web/core/assets";
import { Component, onWillStart, onMounted, onWillUnmount, useRef } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
        onClickSegment: { type: Function, optional: true },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => this.renderChart());
        onWillUnmount(() => this.chart.destroy());
    }

    renderChart() {
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    label: this.props.label,
                    data: Object.values(this.props.data),
                }],
            },
            options: {
                onClick: (event, elements, chart) => {
                    if (elements.length) {
                        const label = chart.data.labels[elements[0].index];
                        this.props.onClickSegment?.(label);
                    }
                },
            },
        });
    }
}
