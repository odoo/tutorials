import { registry } from "@web/core/registry";
import {charField } from "@web/views/fields/char/char_field";


class CharGeneratorField extends charField.component 
{
    static template = "shelter.char_generator_field";
    static props = {...charField.component.props}
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
    ]

    generate()
    {
        const name = CharGeneratorField.names[Math.floor(Math.random() * CharGeneratorField.names.length)];
        console.log(name)
        this.props.record.update({[this.props.name]: name});
    }
    get isShow()
    {
        return !this.props.record.data[this.props.name];
    }
}
export const charFieldGenerator=
{
    ...charField,
    component: CharGeneratorField,
}
registry.category("fields").add("char_generator",charFieldGenerator);

