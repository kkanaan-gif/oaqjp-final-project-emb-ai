#!/bin/bash
# Collect genuine assignment transcripts inside the Skills Network Linux lab.
set -euo pipefail
cd /home/project/final_project
mkdir -p evidence

python3 - <<'PY'
from pathlib import Path
import os
import pty
import subprocess
import sys

root = Path.cwd()
if str(root) != '/home/project/final_project':
    raise SystemExit('Run this in /home/project/final_project in Skills Network.')

def run(commands, filename):
    transcript = ''
    for args in commands:
        import shlex
        transcript += str(root) + ' $ ' + shlex.join(args) + '\n'
        process = subprocess.run(args, text=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
        transcript += process.stdout
        if process.returncode:
            print(transcript)
            (root / 'evidence' / (filename + '.FAILED')).write_text(transcript)
            raise SystemExit('Command failed; no passing evidence was created.')
    (root / 'evidence' / filename).write_text(transcript)
    print(transcript)

inputs = (b'from emotion_detection import emotion_detector\n'
          b"print(emotion_detector('I am really mad about this'))\n"
          b'exit()\n')
sent = False
captured = bytearray()

def provide_input(_fd):
    global sent
    if sent:
        return b''
    sent = True
    return inputs

def capture(fd):
    data = os.read(fd, 4096)
    captured.extend(data)
    return data

status = pty.spawn(['python3'], master_read=capture, stdin_read=provide_input)
interactive = str(root) + ' $ python3\n' + captured.decode(errors='replace')
if os.waitstatus_to_exitcode(status) != 0 or 'Traceback' in interactive:
    (root / 'evidence' / '2b_application_creation.FAILED').write_text(interactive)
    raise SystemExit('Interactive Watson check failed; live evidence is incomplete.')
run([['python3', 'test_emotion_detection.py']], '2b_application_creation')
path = root / 'evidence' / '2b_application_creation'
path.write_text(interactive + path.read_text())
run([['python3', '-c',
      "from emotion_detection import emotion_detector; print(emotion_detector('I am really mad about this'))"]],
    '3b_formatted_output_test')
run([['python3', '-c',
      "from EmotionDetection.emotion_detection import emotion_detector; print(emotion_detector('I am very angry'))"]],
    '4b_packaging_test')
run([['python3', 'test_emotion_detection.py']], '5b_unit_testing_result')
PY
