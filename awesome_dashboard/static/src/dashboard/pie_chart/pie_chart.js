import { Component, t, useProps } from "@odoo/owl";
import { useChart } from "./use_chart";

export class PieChart extends Component {
	static template = "awesome_dashboard.PieChart";
    config = {
        type: 'pie',
    };

    props = useProps({
        values: t.array(),
        labels: t.array(),
    });
    
	setup() {
        this.config.data = {
            labels: this.props.labels,
            datasets: [{
                label: 'My First Dataset',
                data: this.props.values,
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                hoverOffset: 4
            }]
        };

        this.canvasRef = useChart(() => this.config);
	}
}
