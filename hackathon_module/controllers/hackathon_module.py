import glob
import logging
import os
import re
import subprocess
import time
import uuid

from odoo import http
from odoo.http import request
from werkzeug.exceptions import BadRequest

_logger = logging.getLogger(__name__)

RECORDINGS_ROOT = "/home/odoo/odoo-hackathon-recordings"
_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def _concat_chunks_to_webm(chunks, output_path):
    
    """Binary-concatenate raw WebM chunks into one valid WebM file.

    MediaRecorder.start(timeslice) produces chunks where only the first
    one has a valid EBML header (codec init, tracks).  Subsequent chunks
    are bare Cluster continuation segments — not standalone files.
    But when their raw bytes are concatenated in order, the result is a
    single valid WebM that ffmpeg can read as one input.
    """

    with open(output_path, 'wb') as out:
        for chunk in chunks:
            with open(chunk, 'rb') as inp:
                while True:
                    block = inp.read(1 << 20)
                    if not block:
                        break
                    out.write(block)


def _build_ffmpeg_cmd(input_path, output_path):

    """Build an ffmpeg command that re-encodes one WebM into a 360p MP4.

    Flags:
      -r 10           → Drop to 10 frames per second
      -crf 30         → Slightly higher compression threshold
      -preset fast    → Good balance of speed and compression
      scale=640:360   → 360p output
      -c:a aac -b:a 32k -ac 1 → Mono audio at 32kbps (saves massive space)
      +faststart      → MP4 index at front for streaming
    """

    return [
        "ffmpeg", "-y",
        "-i", input_path,
        "-r", "10",
        "-vf", "scale=640:360",
        "-c:v", "libx264", "-crf", "30", "-preset", "fast",
        "-c:a", "aac", "-b:a", "32k", "-ac", "1",
        "-movflags", "+faststart",
        output_path,
    ]


class HackathonController(http.Controller):

    @http.route(['/hackathon/dashboard'], type='http', auth="user", website=True)
    def hackathon_dashboard(self, **kw):
        participant = request.env.user.partner_id
        participant_record = request.env['hackathon.participant'].search([('partner_id', '=', participant.id)], limit=1)
        team = participant_record.team_id
        session = team.session_id
        
        time_left = 0
        if session and session.start_time and session.end_time:
            delta = session.end_time - session.start_time
            time_left = int(delta.total_seconds())

        values = {
            'participant_name': participant.name or '',
            'team_name': str(team.name or ''),
            'time_left': time_left
        }
        return request.render('hackathon_module.hackathon_dashboard_template', values)

    @http.route(['/hackathon/upload_chunk'], type='http', auth="user", methods=['POST'], csrf=False)
    def upload_chunk(self, **kw):

        """Receives one 60-second WebM segment and writes it to disk.
        Called repeatedly while a participant is recording.  Chunks are
        named with a millisecond-timestamp prefix so they sort in
        recording order when finalize_session concatenates them.
        """

        video_file = request.httprequest.files.get('chunk')
        if not video_file:
            raise BadRequest("Missing 'chunk' file in request")

        session_id = kw.get('session_id', '')
        if not session_id or not _SAFE_ID_RE.match(session_id):
            raise BadRequest("Missing or invalid session_id")

        participant = request.env.user.partner_id

        safe_dir = os.path.join(RECORDINGS_ROOT, session_id, str(participant.id))
        os.makedirs(safe_dir, exist_ok=True)
        filename = f"{int(time.time() * 1000)}_{uuid.uuid4().hex}.webm"
        filepath = os.path.join(safe_dir, filename)

        with open(filepath, 'wb') as f:
            video_file.save(f)

        return request.make_json_response({'status': 'ok', 'stored_as': filename})

    @http.route(['/hackathon/finalize_session'], type='http', auth="user", methods=['POST'], csrf=False)
    def finalize_session(self, **kw):
        """Called once when the participant clicks Stop.

        1. Finds all raw .webm chunks on disk (sorted chronologically).
        2. Binary-concatenates them into one combined.webm (this works
           because MediaRecorder chunks are continuation segments of
           one stream — only chunk 1 has the EBML header).
        3. Re-encodes combined.webm into final.mp4 at 240p / 100 kbps.
        4. Deletes the raw chunks and combined.webm to reclaim disk.
        """
        session_id = kw.get('session_id', '')
        if not session_id or not _SAFE_ID_RE.match(session_id):
            raise BadRequest("Missing or invalid session_id")

        participant = request.env.user.partner_id
        safe_dir = os.path.join(RECORDINGS_ROOT, session_id, str(participant.id))

        if not os.path.isdir(safe_dir):
            raise BadRequest("No recording found for this session")

        chunks = sorted(glob.glob(os.path.join(safe_dir, "*.webm")))
        if not chunks:
            raise BadRequest("No chunks found — nothing to finalize")

        combined_webm = os.path.join(safe_dir, "combined.webm")
        _concat_chunks_to_webm(chunks, combined_webm)

        final_mp4 = os.path.join(safe_dir, "final.mp4")
        cmd = _build_ffmpeg_cmd(combined_webm, final_mp4)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

        if result.returncode != 0:
            _logger.error("ffmpeg finalize failed:\n%s", result.stderr)
            return request.make_json_response(
                {'status': 'error', 'message': 'Video processing failed'},
                status=500,
            )
        for chunk in chunks:
            os.remove(chunk)
        if os.path.exists(combined_webm):
            os.remove(combined_webm)

        return request.make_json_response({
            'status': 'ok',
            'final_file': 'final.mp4',
            'path': final_mp4,
        })

    @http.route(['/hackathon/status'], type='jsonrpc', auth="user", website=True)
    def hackathon_status(self, **kw):
        participant = request.env.user.partner_id
        participant_record = request.env['hackathon.participant'].search([('partner_id', '=', participant.id)], limit=1)
        
        if not participant_record:
            return {'status': 'draft', 'session_id': False}
            
        session = participant_record.team_id.session_id or participant_record.session_id
        if not session:
            return {'status': 'draft', 'session_id': False}
        session_id = f"sess_{session.id}_{session.name}".replace(" ", "_")
        return {
            'status': session.state,
            'session_id': session_id
        }
