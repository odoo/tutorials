import publicWidget from "@web/legacy/js/public/public_widget";

const CHUNK_INTERVAL_MS = 60000;
const VIDEO_BITS_PER_SECOND = 300_000;

publicWidget.registry.HackathonRecorder = publicWidget.Widget.extend({
    selector: ".o_hackathon_dashboard",
    events: {
        "click #acceptConsentBtn": "_onAcceptConsent",
    },

    init() {
        this._super(...arguments);
        this.stream = null;
        this.timer = null;
        this.pollingInterval = null;
        this.timeLeft = 0;
        this.sessionId = null;
        this._uploadPromises = [];
        this.isRecording = false;
    },

    start() {
        this.videoEl = this.el.querySelector("#webcamPreview");
        this.timerEl = this.el.querySelector("#timerDisplay");
        this.startBtn = this.el.querySelector("#startBtn");
        this.stopBtn = this.el.querySelector("#stopBtn");
        
        const dataTimeLeft = parseInt(this.el.dataset.timeLeft);
        if (!isNaN(dataTimeLeft)) {
            this.timeLeft = dataTimeLeft;
        }
        
        this._renderTimer();
        
        // Show consent modal on load using jQuery (standard for Odoo legacy widgets)
        const $modal = this.$("#consentModal");
        if ($modal.length) {
            $modal.modal("show");
        } else {
            console.error("CRITICAL: Consent Modal not found inside o_hackathon_dashboard! Make sure the module was upgraded.");
        }
        
        return this._super(...arguments);
    },

    destroy() {
        clearInterval(this.timer);
        clearInterval(this.pollingInterval);
        this.stream?.getTracks().forEach((t) => t.stop());
        this._super(...arguments);
    },

    _renderTimer() {
        const pad = (n) => String(Math.floor(n)).padStart(2, "0");
        this.timerEl.textContent =
            `${pad(this.timeLeft / 3600)}:${pad((this.timeLeft % 3600) / 60)}:${pad(this.timeLeft % 60)}`;
    },
    
    async _onAcceptConsent() {
        if (!("MediaRecorder" in window)) {
            this._notify("Not supported", "This browser cannot record video. Please use Chrome, Edge, or Firefox.", "danger");
            return;
        }

        try {
            // Request permissions right away
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 640 }, height: { ideal: 360 } },
                audio: true,
            });
            if (this.videoEl) {
                this.videoEl.srcObject = this.stream;
            }
            
            this.$("#consentModal").modal("hide");
            
            // Start polling backend for hackathon status
            this.pollingInterval = setInterval(() => this._pollStatus(), 5000);
            this._pollStatus(); // Call immediately
            
            this._notify("Ready", "Permissions granted. Waiting for admin to start the hackathon.", "info");
            
        } catch (err) {
            console.error(err);
            this._notify("Camera/Mic Error", "Could not access webcam/microphone. You must allow permissions.", "danger");
        }
    },
    
    _notify(title, message, type="info") {
        console.log(`[${title}] ${message}`);
        if (type === 'danger' || type === 'success') {
            // Only alert on critical issues or final success
            alert(`${title}: ${message}`);
        }
    },
    
    async _pollStatus() {
        try {
            const response = await fetch("/hackathon/status", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ jsonrpc: "2.0", method: "call", params: {} }),
            });
            const data = await response.json();
            const result = data.result;
            
            if (result && result.status === 'in_progress' && !this.isRecording) {
                this._onStartRecording(result.session_id);
            } else if (result && result.status === 'done' && this.isRecording) {
                this._onStopRecording();
            }
        } catch (err) {
            console.warn("Polling error", err);
        }
    },

    _uploadChunk(blob) {
        const formData = new FormData();
        formData.append("chunk", blob, `${Date.now()}.webm`);
        formData.append("session_id", this.sessionId);
        const promise = fetch("/hackathon/upload_chunk", {
            method: "POST",
            body: formData,
        }).then((response) => {
            if (!response.ok) {
                console.warn("Chunk upload failed with status", response.status);
            }
        }).catch((err) => {
            console.warn("Chunk upload failed:", err);
        });

        this._uploadPromises.push(promise);
        return promise;
    },
    
    async _finalizeSession() {
        try {
            const formData = new FormData();
            formData.append("session_id", this.sessionId);

            const response = await fetch("/hackathon/finalize_session", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                this._notify("Recording saved", "Your session video has been saved successfully.", "success");
            } else {
                console.warn("Finalize failed with status", response.status);
            }
        } catch (err) {
            console.warn("Finalize request failed:", err);
        }
    },


    _onStartRecording(sessionId) {
        if (!this.stream) return;
        
        this.isRecording = true;
        this.sessionId = sessionId;

        const mime = ["video/webm;codecs=vp9", "video/webm"].find((t) =>
            MediaRecorder.isTypeSupported(t)
        ) || "video/webm";

        this.recorder = new MediaRecorder(this.stream, {
            mimeType: mime,
            videoBitsPerSecond: VIDEO_BITS_PER_SECOND,
            audioBitsPerSecond: 64000,
        });

        this.recorder.ondataavailable = (e) => {
            if (e.data.size > 10000) {
                this._uploadChunk(e.data);
            }
        };
        this.recorder.start(CHUNK_INTERVAL_MS);

        this.timer = setInterval(() => {
            if (this.timeLeft > 0) {
                this.timeLeft--;
                this._renderTimer();
            } else {
                this._onStopRecording();
            }
        }, 1000);
        
        this._notify("Started", "The hackathon has started. Recording in progress.", "info");
    },

    _onStopRecording() {
        this.isRecording = false;
        if (this.recorder?.state !== "inactive") {
            this.recorder.onstop = async () => {
                await Promise.all(this._uploadPromises);
                this._finalizeSession();
            };
            this.recorder.stop();
        }
        clearInterval(this.timer);
        this.timeLeft = 0;
        this._renderTimer();
        clearInterval(this.pollingInterval);
        
        this._notify("Finished", "Hackathon is complete. Processing final video.", "info");
    },
});
