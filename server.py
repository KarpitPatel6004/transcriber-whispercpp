import os
from waitress import serve
import utils
from config import Config
import celery_tasks
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def index():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    # If the user does not select a file, browser also submit an empty part without filename
    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the uploaded file
        task_id = utils.generate_unique_id()
        filename = os.path.join(Config.UPLOAD_FOLDER, task_id + "-" + file.filename)

        ######
        # code to upload file in cloud
        ######

        file.save(filename)
        filename, audio_length = utils.preprocess_audio(filename)

        if Config.ALLOW_MULTIPLE_QUEUE:
            if audio_length > 30:
            # Transcribe the audio file
                task = celery_tasks.long_running_tasks.apply_async(args=[filename], task_id=task_id)
            else:
                task = celery_tasks.short_running_tasks.apply_async(args=[filename], task_id=task_id)
        else:
            task = celery_tasks.short_running_tasks.apply_async(args=[filename], task_id=task_id)

        # Return the task ID to the user
        return jsonify({"task_id": task.id, "audio_length": audio_length, "file": filename})


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)