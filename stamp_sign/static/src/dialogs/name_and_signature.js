import { renderToString } from "@web/core/utils/render";
import { patch } from "@web/core/utils/patch";
import { NameAndSignature } from "@web/core/signature/name_and_signature";
import { rpc } from "@web/core/network/rpc";
import { onWillStart } from "@odoo/owl";

patch(NameAndSignature.prototype, {

    setup() {
        super.setup(...arguments);

        onWillStart(async () => {
            this.Notofonts = await rpc(`/web/sign/get_fonts/NotoSans-Reg.ttf`);
        });

    },

    async drawCurrentName() {
        if (this.props.signatureType === "stamp") {
            const font = this.Notofonts;
            const stamp = this.getStampDetails();
            const canvas = this.signatureRef.el;
            const img = this.getSVGStamp(font, stamp, canvas.width, canvas.height);
            await this.printImage(img);
        }
        else {
            super.drawCurrentName()
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
            logo: this.props.signature.logo,
        }
    },
    /**
     * @private
     * @param {string} font: base64 encoded font to use
     * @param {string} text: the name to draw
     * @param {number} width: the width of the resulting image in px
     * @param {number} height: the height of the resulting image in px
     * @returns {string} image = mimetype + image data
     */
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
            logo: stampData.logo
        });
        return "data:image/svg+xml," + encodeURI(svg)
    },

    onInputStampDetails(ev) {
        if (ev.target.name === "logo") {
            const file = ev.target.files[0];
            if (file && this.state.signMode === "auto") {
                const reader = new FileReader();
                reader.onload = () => {
                    this.props.signature.logo = reader.result;
                    this.drawCurrentName();
                };
                reader.readAsDataURL(file)
            }
        }
        else {
            this.props.signature[ev.target.name] = ev.target.value;
        }
        if (!this.state.showSignatureArea && this.getStampData()) {
            this.state.showSignatureArea = true;
        }
        if (this.state.signMode === "auto") {
            this.drawCurrentName();
        }
    },
})
