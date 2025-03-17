/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { MobileAadharDialog } from "../dialogs/mobile_aadhaar_dialog";
import { SignablePDFIframe } from "@sign/components/sign_request/signable_PDF_iframe";

patch(SignablePDFIframe.prototype, {

    setup() {
        this.signInfo = useService("signInfo");
        this.dialog = useService("dialog");
        this.ui = useService("ui")
    },

    async getAuthDialog() {
        if (this.props.authMethod === 'aadhar_esign') {
            return {
                component: MobileAadharDialog,
                props: {
                    onSubmit: async (userData) => {
                        this.signInfo.set("mobileNumber", userData.mobile);
                        this.signInfo.set("aadhaarNumber", userData.aadhaar);
                        this.ui.block();
                        await this.fetchSignedDocument(userData.mobile, userData.aadhaar);
                        this.ui.unblock();
                    }
                }
            }
        }
        return super.getAuthDialog();
    },

    generateVerificationId(length = 10) {
        const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        let verificationId = "";
        for (let i = 0; i < length; i++) {
            verificationId += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        return verificationId;
    },

    async fetchSignedDocument(mobile, aadhaar) {

        const req_id = this.signInfo.get("documentId");
        const token = this.signInfo.get("signRequestToken");
        const url1 = `/sign/data/${req_id}/${token}`;
        const url2 = `/sign/file/${req_id}/${token}`;

        try {
            const data1 = await fetch(url1, {
                method: "GET",
            });
            const data2 = await fetch(url2, {
                method: "GET",
            });
            const response = await data1.json();
            const pdfBlob = await data2.blob();
            const formData = new FormData();
            formData.append("document", pdfBlob, response.filename); 
            const uploadResponse = await fetch("/sign/upload_document", {
                method: "POST",
                body: formData,
            });
            const result = await uploadResponse.json();
            const verification_id = this.generateVerificationId()
            const expiry_days = response.expiry_in_days
            const redirect_url = "";
            const signers = response.signers.map((signer, index) => ({
                name: signer.name,
                email: signer.email,
                sequence: index + 1, 
                sign_positions: signer.sign_positions.map(pos => ({
                    page: pos.page,
                    top_left_x_coordinate: pos.top_left_X,
                    bottom_right_x_coordinate: pos.bottom_right_X,
                    top_left_y_coordinate: pos.top_left_Y,
                    bottom_right_y_coordinate: pos.bottom_right_Y
                })),
                phone: mobile, 
                aadhaar_last_four_digit: aadhaar
            }));
            if (result.document_id) {
                this.sendSignerDetails(verification_id, result.document_id, expiry_days, signers, redirect_url);
            }   
        } catch (error) {
            console.log(error)
        } 
    },  

    async sendSignerDetails(verification_id, document_id, expiry_in_days, signers, redirect_url) {
        try {
            const response = await fetch("/e_sign/create_request", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    verification_id: verification_id,
                    document_id: document_id,
                    expiry_days: expiry_in_days,
                    signers: signers,
                    redirect_url: redirect_url
                }),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const responseData = await response.json();
            if (responseData.signing_link) {
                const signingLink = responseData.signing_link;
                const newTab = window.open(signingLink, '_blank');
                this.ui.block();
                const interval = setInterval(() => {
                    if (newTab.closed) {
                        clearInterval(interval);
                        window.focus();
                        this.verifyEsignature(verification_id); 
                    }
                }, 1000);  
            } else {
                console.error("Signing link not found in response!");
            } 
        } catch (error) {
            console.error("Error sending signer details:", error);
        }
    },

    async verifyEsignature(verification_id) {
        try {
            const response = await fetch(`/sign/verify_esignature?verification_id=${verification_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const responseData = await response.json();
            this.ui.unblock();
            if (responseData.status == 'SUCCESS') {               
                this._sign();
            } else {
                this.dialog.add(ConfirmationDialog, {
                    title: _t("Verification Failed"),
                    body: "Your signature verification process via Cashfree portal could not be completed. Please try again..."
                });
            }
            return responseData;
        } catch (error) {
            console.error("Error verifying e-signature:", error);
            alert("An error occurred while verifying e-signature.");
        }
    }, 
});
