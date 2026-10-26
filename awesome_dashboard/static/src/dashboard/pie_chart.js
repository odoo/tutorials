import { Component, onWillStart, signal, t, useEffect, usePlugin, useProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useChart } from "./use_chart";
import { ActionPlugin } from "@web/webclient/actions/action_plugin";

const SIZE_COLORS = {
    s: "#36A2EB",
    m: "#FF6384",
    l: "#4BC0C0",
    xl: "#FF9F40",
    xxl: "#9C6DF4",
};

export class PieChart extends Component {

    static template = "awesome_dashboard.PieChart";

    action = usePlugin(ActionPlugin);

    props = useProps({
        label: t.string(),
        data: t.object(),
    })

    canvasRef = useChart(() => {
        const keys = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = keys.map((key) => SIZE_COLORS[key]);
        return {
            type: "pie",
            data: {
                label: keys,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color,
                    }
                ]
            },
            options: {
                maintainAspectRatio: false,
                onClick: (_events, elements) => {
                    const clickedElement = elements[0];
                    const datasetIndex = clickedElement.index;
                    const _label = keys[datasetIndex];
                    const _labelValue = data[datasetIndex];
                },
            }
        }
    });

}   