import { Component, useProps, types as t } from "@odoo/owl";
import { useChart } from "../use_chart";

const SIZE_COLORS = {
    s: "#36A2EB",
    m: "#FF6384",
    l: "#4BC0C0",
    xl: "#FF9F40",
    xxl: "#9C6DF4",
};

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    props = useProps({
        label: t.string(),
        data: t.object(),
    });

    canvasRef = useChart(() => {
        const keys = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = keys.map((key) => SIZE_COLORS[key]);
        return {
            type: "pie",
            data: {
                labels: keys,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
            options: {
                maintainAspectRatio: false,
            },
        };
    });
}
