import {
    Component,
    onWillStart,
    useRef,
    onMounted,
    onWillUnmount,
} from '@odoo/owl';
import { loadJS } from '@web/core/assets';
import { getColor } from '@web/core/colors/colors';

export class PieChart extends Component {
    static template = 'awesome_dashboard.PieChart';
    static props = {
        label: {
            type: String,
            optional: true,
        },
        data: {
            type: Object,
            optional: true,
        },
    };

    setup() {
        this.canvasRef = useRef('canvas');
        this.chart = null;
        this.renderChart = this.renderChart.bind(this);
        this.getChartData = this.getChartData.bind(this);
        onWillStart(() => loadJS('/web/static/lib/Chart/Chart.js'));
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
        onMounted(() => {
            this.renderChart();
        });
    }

    getChartData() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const colors = labels.map((_, index) => getColor(index * 2 + 1));
        const chartData = {
            labels,
            datasets: [
                {
                    label: this.props.label,
                    data,
                    backgroundColor: colors,
                    hoverOffset: 1,
                },
            ],
        };
        return chartData;
    }

    renderChart() {
        const config = {
            type: 'pie',
            data: this.getChartData(),
        };
        this.chart = new Chart(this.canvasRef.el, config);
    }
}
