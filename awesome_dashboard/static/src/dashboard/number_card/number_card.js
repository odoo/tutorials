import { Component, t, useProps }  from "@odoo/owl";
import { DashboardItem } from "../dashboard_item";

export class NumberCard extends Component {
    static template = 'awesome_dashboard.NumberCard';
    components = { DashboardItem };

    props = useProps({
        title: t.string(),
        value: t.number(),
        description: t.string().optional(""),
    });
}

export default NumberCard;
