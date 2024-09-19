import { registry } from "@web/core/registry";
import { many2OneField } from "@web/views/fields/many2one/many2one_field";
import { imageUrl } from "@web/core/utils/urls";


class AnimalTypeManyToOne extends many2OneField.component {

    static template = "shelter.AnimalTypeManyToOne";
    static props = { ...many2OneField.component.props, imageField: { type: String } };

    get pictogramUrl() {
        return imageUrl(this.props.record.resModel, this.props.record.resId, this.props.imageField);
    }

    get hasImage() {
        return Boolean(this.props.record.data[this.props.imageField]);
    }

}

const animalTypeManyToOne = {
    ...many2OneField,
    component: AnimalTypeManyToOne,
    fieldDependencies: [...many2OneField.fieldDependencies || [], { name: "pictogram", type: "image" }],
    extractProps({options}) {
        const props = many2OneField.extractProps(...arguments);
        props.imageField = options.image_field;
        return props;
    }
}

registry.category("fields").add("animal_type_many2one", animalTypeManyToOne);
