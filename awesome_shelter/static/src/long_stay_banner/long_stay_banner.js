import { Component } from "@odoo/owl";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
import { registry } from "@web/core/registry";

class LongStayBanner extends Component {
    static template = "shelter.long_stay_banner";
    static props = { 
        ...standardWidgetProps
    };
}
export const longStayBanner=
{
    component: LongStayBanner,
}
registry.category("view_widgets").add("long_stay_banner",longStayBanner);

