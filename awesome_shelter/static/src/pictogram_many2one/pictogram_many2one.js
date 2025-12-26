import { registry } from "@web/core/registry";
import {Many2OneField, buildM2OFieldDescription } from "@web/views/fields/many2one/many2one_field";
import { imageUrl } from "@web/core/utils/urls";


const field = buildM2OFieldDescription(Many2OneField);

class PictoMany2One extends Many2OneField 
{
    static template = "shelter.picto_many2one";
    static props = {
        ...Many2OneField.props,
        image: {optional : true, type: String}
    };

    get pictoUrl()
    {
        console.log(this.props.record.resModel)
        console.log(this.props.record.resId)
        console.log(this.props.image)
        console.log(imageUrl(this.props.record.resModel, this.props.record.resId, this.props.image));
    return imageUrl(this.props.record.resModel, this.props.record.resId, this.props.image);
    }
    get hasImage()
    {
        return Boolean(this.props.record.data[this.props.image]);
    }

}


const pictoMany2One = {
    ...field,
    component: PictoMany2One,
    fieldDependencies: [...field.fieldDependencies || [], {name: "pictogram", type:"image"}],
    extractProps({options})
    {
        const props = field.extractProps(...arguments)
        props.image = options.image;
        return props;
    },
}
registry.category("fields").add("picto_many2one",pictoMany2One);
