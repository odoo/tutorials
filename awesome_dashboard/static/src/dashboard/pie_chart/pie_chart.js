import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import {
    Component,
    onWillStart,
    useRef,
    onMounted,
    onWillUnmount,
    onWillUpdateProps,
} from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.AwesomePieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => {
            this.renderChart();
        });
        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this.updateChart(nextProps.data);
            }
        });
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const colors = labels.map((_, index) => getColor(index));

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels,
                datasets: [
                    {
                        label: this.props.label,
                        data,
                        backgroundColor: colors,
                    },
                ],
            },
        });
    }

    updateChart(newData) {
        const labels = Object.keys(newData);
        const data = Object.values(newData);

        this.chart.data.labels = labels;
        this.chart.data.datasets[0].data = data;
        this.chart.update();
    }
}
