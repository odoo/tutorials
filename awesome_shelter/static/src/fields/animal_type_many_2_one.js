import { registry } from "@web/core/registry";
import { Many2OneField, buildM2OFieldDescription } from "@web/views/fields/many2one/many2one_field";
import { imageUrl } from "@web/core/utils/urls";

const field = buildM2OFieldDescription(Many2OneField);

class AnimalTypeManyToOne extends Many2OneField {

    static template = "shelter.AnimalTypeManyToOne";
    static props = { ...Many2OneField.props, imageField: { type: String } };

    get pictogramUrl() {
        return imageUrl(this.props.record.resModel, this.props.record.resId, this.props.imageField);
    }

    get hasImage() {
        return Boolean(this.props.record.data[this.props.imageField]);
    }

}

const animalTypeManyToOne = {
    ...field,
    component: AnimalTypeManyToOne,
    fieldDependencies: [...field.fieldDependencies || [], { name: "pictogram", type: "image" }],
    extractProps({options}) {
        const props = field.extractProps(...arguments);
        props.imageField = options.image_field;
        return props;
    }
}

registry.category("fields").add("animal_type_many2one", animalTypeManyToOne);
