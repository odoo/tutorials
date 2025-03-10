import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";


Orderline.props = {
    ...Orderline.props,
    line: {
        ...Orderline.props.line,
        shape: {
            ...Orderline.props.line.shape,
            barcode: { type: String, optional: true },
            standardPrice: { type: String, optional: true},
            showStrikedPrice: { type: Boolean, optional: true}
        },
    },
};
