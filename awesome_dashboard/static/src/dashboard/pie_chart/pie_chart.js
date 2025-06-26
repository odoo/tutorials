import { Component, onMounted, onWillUpdateProps, onWillStart, onWillUnmount, useRef } from "@odoo/owl";
import { loadJS  } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.canvas = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

        onMounted(() => {
            this.renderPieChart(this.props);
        });

        onWillUpdateProps((nextProps) => {
            this.chart.destroy();
            this.renderPieChart(nextProps);
        });

        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderPieChart(props) {
        const labels = Object.keys(props.data);
        const values = Object.values(props.data);
        this.chart = new Chart(this.canvas.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    label: props.label,
                    data: values,
                }],
            },
        });
    }
}