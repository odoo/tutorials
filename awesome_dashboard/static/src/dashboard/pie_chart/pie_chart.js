import { Component, useRef, onMounted, onWillStart, onWillUnmount, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        'data': {
            type: Object,
        },
    };
    
    setup() {
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        this.chartRef = useRef("chart");
        onMounted(() => {
            this.renderChart();
        });
        onWillUpdateProps((props) => {
            this.chart.data.datasets[0].data = Object.values(props.data);
            this.chart.update();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
        this.action = useService("action");
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        this.chart = new Chart(this.chartRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: Object.values(this.props.data),
                }],
            },
            options: {
                onClick: (ev, elements) => {
                    if (elements.length > 0) {
                        const index = elements[0].index;
                        const clickedLabel = labels[index];
                        this.openOrderListView(clickedLabel)
                    }
                }
            }
        });
    };

    openOrderListView(size) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t(`Orders with size ${size}`),
            res_model: "sale.order",
            views: [
                [false, 'list'],
                [false, 'form'],
            ],
            domain: [["name", "=", size]],
        });
    }
}
