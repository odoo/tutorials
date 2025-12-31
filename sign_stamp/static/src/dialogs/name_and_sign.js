import { renderToString } from "@web/core/utils/render";
import { patch } from "@web/core/utils/patch";
import { NameAndSignature } from "@web/core/signature/name_and_signature";

patch(NameAndSignature.prototype, {
    async drawCurrentName() {
        if (this.props.signatureType === "stamp") {
            const font = this.fonts[this.currentFont];
            const stamp = this.getStampDetails();
            const canvas = this.signatureRef.el;
            const img = this.getSVGStamp(font, stamp, canvas.width, canvas.height);
            await this.printImage(img);
        } else {
            super.drawCurrentName();
        }
    },

    getStampDetails() {
        return {
            name: this.props.signature.name,
            company: this.props.signature.company,
            address: this.props.signature.address,
            city: this.props.signature.city,
            country: this.props.signature.country,
            vat: this.props.signature.vat,
            image: this.props.signature.image,
        };
    },

    getSVGStamp(font, stampData, width, height) {
        const svg = renderToString("stamp_sign.sign_svg_stamp", {
            width: width,
            height: height,
            font: font,
            name: stampData.name,
            company: stampData.company,
            address: stampData.address,
            city: stampData.city,
            country: stampData.country,
            vat: stampData.vat,
            image: stampData.image,
        });
        return "data:image/svg+xml," + encodeURI(svg);
    },
});
