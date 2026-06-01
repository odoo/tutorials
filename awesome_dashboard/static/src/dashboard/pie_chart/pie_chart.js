import {loadJS} from "@web/core/assets";
import {getColor} from "@web/core/colors/colors";
import {Component, onMounted, onWillStart, onWillUnmount, useRef} from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        // Load Chart.js before mounting the component
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => this.renderChart());
        onWillUnmount(() => {
            if (this.chart) this.chart.destroy();
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const values = Object.values(this.props.data);
        const colors = labels.map((_, i) => getColor(i));
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    label: this.props.label,
                    data: values,
                    backgroundColor: colors,
                }],
            },
        });
    }
}
