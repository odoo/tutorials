import {
    Component,
    onMounted,
    onWillStart,
    onWillUnmount,
    onWillUpdateProps,
    useRef,
} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

      onMounted(() => {
            this.chart = new globalThis.Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    labels: Object.keys(this.props.data).map((size) => size.toUpperCase()),
                    datasets: [
                        {
                            data: Object.values(this.props.data),
                            backgroundColor: ["#0d6efd", "#ffc107", "#198754"],
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                },
            });
        });

        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this.chart.data.labels = Object.keys(nextProps.data).map((size) =>
                    size.toUpperCase()
                );
                this.chart.data.datasets[0].data = Object.values(nextProps.data);
                this.chart.update();
            }
        });

        onWillUnmount(() => this.chart?.destroy());
    }
}
