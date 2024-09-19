import { standardFieldProps } from "@web/views/fields/standard_field_props"
import { registry } from "@web/core/registry"
import { charField } from "@web/views/fields/char/char_field";

class NameGeneratorField extends charField.component {
    static template = "shelter.NameGeneratorField";
    static props = { ...charField.component.props };
    static names = [
        "Charlie",
        "Daisy",
        "Bella",
        "Lola",
        "Luna",
        "Milo",
        "Teddy",
        "Cooper",
        "Max",
        "Bailey",
        "Buddy",
        "Coco",
        "Leo",
        "Loki",
        "Lucy",
        "Chloé",
        "Oscar",
        "Rocky",
        "Sadie",
        "Bonnie",
        "Poppy",
    ];

    generate() {
        const name = NameGeneratorField.names[Math.floor(Math.random() * NameGeneratorField.names.length)];
        this.props.record.update({ [this.props.name]: name });
    }

    get shouldShowButton() {
        return !this.props.record.data[this.props.name];
    }
}

const nameGeneratorField = {
    ...charField,
    component: NameGeneratorField,
}

registry.category("fields").add("name_generator", nameGeneratorField);
