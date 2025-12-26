import { registry } from "@web/core/registry";
import { statusBarField } from "@web/views/fields/statusbar/statusbar_field";
import { useService } from "@web/core/utils/hooks";


class AdoptedStatusBar extends statusBarField.component
{
    static props = {...statusBarField.component.props, activationStage:{type : String}}
    static template = statusBarField.component.template;

    setup()
    {
        super.setup();
        this.effect = useService("effect");
    }
    async selectItem(item)
    {
        super.selectItem(item);
        if(item.value == this.props.activationStage)
        {
            this.effect.add({message : "A new happy life on the makeing !!"});
        }

    }

}

export const adoptedStatusBar =
    {
        ...statusBarField,
        component: AdoptedStatusBar,
        extractProps({options})
        {
            const props = statusBarField.extractProps(...arguments);
            props.activationStage = options.activationStage
            return props;
        }
    }

registry.category("fields").add("adopt_status_bar",adoptedStatusBar);
