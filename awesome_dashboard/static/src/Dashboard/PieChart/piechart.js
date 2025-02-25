import { Component, onMounted , onWillStart, onWillUnmount, useEffect, useRef} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class Piechart extends Component {
    static template = "awesome_dashboard.PieChart"
    static props = {
        data: Object
    }

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"))
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(this.onWillUnmount);
        useEffect(
            // when data changes chartdata will change 
            () => { this.renderChart(); },
            () => [this.props.data] 
        );
    }

    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        if (!this.props.data || !this.canvasRef.el) {
            return
        }
        const lables = Object.keys(this.props.data);
        const data = Object.values(this.props.data);

        this.chart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                datasets:[{
                    data: data,
                }],
                labels: lables
            }
        });
    }
}
