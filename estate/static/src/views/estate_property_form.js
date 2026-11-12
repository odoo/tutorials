import {registry} from "@web/core/registry";
import {formView} from "@web/views/form/form_view";

class EstatePropertyFormRecord extends formView.Model.Record {
    /**
     * @override
     */
    async _save() {
        if (this.resModel !== "estate.property") {
            return super._save(...arguments);
        }
        try {
            if (this.data.state === "sold") {
                await this.model.orm.call(
                    "estate.property",
                    "action_sold_property",
                    [[this.resId]]
                );

                this.model.effect.add({
                    message: "Congratulations! This property is sold.",
                    type: "rainbow_man",
                });
            } else if (this.data.state === "cancelled") {
                await this.model.orm.call(
                    "estate.property",
                    "action_cancel_property",
                    [[this.resId]]
                );
            }
            return await super._save(...arguments);
        } catch (error) {
            throw error;
        }
    }

}

class EstatePropertyFormModel extends formView.Model {
    static Record = EstatePropertyFormRecord;
    static services = [...formView.Model.services, "effect"];

    setup(params, services) {
        super.setup(...arguments);
        this.effect = services.effect;
    }
}

registry.category("views").add("estate_property_form", {
    ...formView,
    Model: EstatePropertyFormModel,
});
