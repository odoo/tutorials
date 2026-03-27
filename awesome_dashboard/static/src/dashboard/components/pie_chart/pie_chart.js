import {Component, onMounted, onWillStart, onWillUnmount, onWillUpdateProps, useRef} from "@odoo/owl";
import {loadJS} from "@web/core/assets";
import {useService} from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: Object,
        onClick: {type: Function, optional: true},
    }

    setup() {
        super.setup();

        this.canvasRef = useRef("chartCanvas");
        this.action = useService("action");

        this.chart = null;

        onWillStart(async () => {
            await loadJS(["/web/static/lib/Chart/Chart.js"]);
        });

        onMounted(() => {
            if (this.chart) {
                this.chart.destroy();
            }

            this.chart = new Chart(this.canvasRef.el, this._getChartConfig());
        })

        onWillUpdateProps(nextProps => {
            this.chart.data.labels = [...Object.keys(nextProps.data)];
            this.chart.data.datasets.forEach((dataset) => {
                dataset.data = Object.values(nextProps.data);
            });

            this.chart.update();
        });

        onWillUnmount(this.onWillUnmount);
    }

    onWillUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    _getChartConfig() {
        return {
            type: 'pie',
            data: {
                labels: [...Object.keys(this.props.data)],
                datasets: [{
                    data: Object.values(this.props.data),
                    backgroundColor: [
                        'yellow', 'salmon', 'green',
                    ],
                    borderWidth: 1,
                    hoverOffset: 4,
                }]
            },
            options: {
                events: ['click'],
            },
            plugins: [{
                id: 'customEventCatcher',
                beforeEvent: (chart, args) => {
                    if (args?.event.type === 'click') {
                        const [activeElement] = chart.getElementsAtEventForMode(args.event, 'nearest', {intersect: true}, true);
                        const index = activeElement.index;

                        if (this.props.onClick) {
                            this.props.onClick(this.action, Object.keys(this.props.data)[index]);
                        }
                    }
                }
            }],
        }
    }
}