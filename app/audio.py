"""Audio file handling via MongoDB GridFS — zero external dependencies."""
import io
from bson import ObjectId
import gridfs
from flask import Blueprint, send_file, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.extensions import csrf

audio_bp = Blueprint("audio", __name__)
csrf.exempt(audio_bp)

ALLOWED_EXT = {"mp3", "ogg", "wav", "m4a", "aac", "webm"}


def _get_fs():
    """Get GridFS bucket for the cefr_mock database."""
    from app.extensions import mongo
    return gridfs.GridFS(mongo.db)


@audio_bp.route("/upload", methods=["POST"])
def upload_audio():
    """Upload audio file → GridFS → return file_id + URL."""
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files["file"]
    if file.filename == "" or not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXT:
        return jsonify({"error": f"Not allowed: .{ext}. Allowed: {', '.join(sorted(ALLOWED_EXT))}"}), 400

    fs = _get_fs()
    data = file.read()
    fid = fs.put(data, filename=secure_filename(file.filename), content_type=file.content_type or f"audio/{ext}")
    return jsonify({
        "file_id": str(fid),
        "url": f"/audio/get/{fid}",
        "filename": file.filename
    })


@audio_bp.route("/get/<file_id>")
def get_audio(file_id):
    """Serve audio file from GridFS."""
    try:
        fs = _get_fs()
        grid_file = fs.get(ObjectId(file_id))
        data = grid_file.read()
        ct = grid_file.content_type or "audio/mpeg"
        return send_file(
            io.BytesIO(data),
            mimetype=ct,
            as_attachment=False,
            download_name=grid_file.filename or "audio.mp3"
        )
    except Exception:
        return "Audio not found", 404
