import {Component, onWillStart, onMounted, xml, useRef, onWillUpdateProps} from "@odoo/owl";
import {loadJS} from "@web/core/assets";

export class PieChartCard extends Component {
    static template = xml`
        <h5 class="card-title"><t t-esc="props.title" /></h5>
        <p class="card-text">
            <div style="text-align: center;">
                <canvas t-ref="pieChartCanvas" />
            </div>
        </p>
`
    static props = {
        data: {optional: true},
        title: {type: String, optional: true},
    }
    static defaultProps = {
        size: 1,
    };

    setup() {
        this.canvas = useRef('pieChartCanvas');
        this.chart = null;
        onWillStart(async () => {
            this.chartjs = await loadJS("/web/static/lib/Chart/Chart.js")

        })
        onWillUpdateProps(this.renderChart);
        onMounted(this.renderChart);
    }

    renderChart() {
        {
            if (!this.canvas.el) {
                console.log("canvas not found")
                return
            }
            console.log(this.canvas);
            const ctx = this.canvas.el.getContext('2d');

            console.log(this.props.data)
            if (!this.props.data) {
                console.log("piechart No data");
                return
            }
            if (!this.chart) {
                this.chart = new Chart(ctx, {
                    type: 'pie', data: {
                        labels: ['m', 'xl', 's'],
                        // labels: Object.keys(this.props.data),
                        data: [this.props.data.m, this.props.data.xl, this.props.data.s],
                        "datasets": [{
                            "label": "Tshirts Dataset",
                            // data: Object.values(this.props.data),
                            // Hardcode the data so it stay in the same order on update
                            "data": [this.props.data.m, this.props.data.xl, this.props.data.s],
                        }],
                    },
                });
            } else {
                // console.log(this.chart)
                // console.log('data', [this.props.data.m, this.props.data.xl, this.props.data.s])
                this.chart.data.datasets[0].data = [this.props.data.m, this.props.data.xl, this.props.data.s];
                this.chart.update();
            }
        }
    }


}