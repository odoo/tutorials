import { Component } from "@odoo/owl"
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
import { registry } from "@web/core/registry";


class LongStayBannerWidget extends Component {

    static template = "shelter.LongStayBannerWidget";
    static props = { ...standardWidgetProps }

    get animalName () {
        return this.props.record.data["display_name"];
    }

}

const longStayBannerWidget = {
    component: LongStayBannerWidget,
}

registry.category("view_widgets").add("long_stay_banner", longStayBannerWidget);
