from functools import reduce

from datetime import datetime
from re import I
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas as canv
from reportlab.lib.pagesizes import A4, landscape

import tempfile
import base64

from plable.components import Parallel

CELL_SCALE = 3
MAX_WIDTH = 400
SCALE = 16
RECT_OFFSET = 0
COLOR = {"LECTURE": (1, 1, 0), "TUTORIAL": (1, 0, 1), "LABORATORY": (0, 1, 1)}
EVENT_TYPE = {"LECTURE": "Lec.", "TUTORIAL": "Tut.", "LABORATORY": "Lab."}


event_pos = lambda x: SCALE * (x / MAX_WIDTH) * cm


event_height = (
    lambda col, parity: (5 - col + 0.5 if parity == "EVEN" else 5 - col) * CELL_SCALE * cm
)
event_size = lambda parity: (CELL_SCALE if parity == "BOTH" else CELL_SCALE / 2) * cm


def render_day_grid(canvas):
    dow = ['MON', 'TUE', 'WED', 'THU', 'FRI',''][::-1]
    canvas.setFont("Helvetica", 8)

    for i in range(6):
        canvas.line(0, i * cm * CELL_SCALE, MAX_WIDTH * cm, i * cm * CELL_SCALE)
        canvas.drawString(-0.8 * cm, (i-0.5) * cm * CELL_SCALE, dow[i])

    # add vertical lines?


def render_event(canvas, day, start, end, type, course, parity, parallel_no):
    day = int(day)
    event_time = f"{start[:5]}-{end[:5]}"
    origin = datetime.strptime("07:30:00", "%H:%M:%S")
    start = (datetime.strptime(start, "%H:%M:%S") - origin).seconds // 60
    end = (datetime.strptime(end, "%H:%M:%S") - origin).seconds // 60

    canvas.setFillColorRGB(*COLOR[type], alpha=0.5)
    # event rectangle
    canvas.rect(
        event_pos(start),  # X origin
        event_height(day, parity),  # Y
        event_pos(end - start),  # X target
        event_size(parity),
        fill=1,
    )
    canvas.setFillColorRGB(0, 0, 0)

    # duration
    canvas.setFont("Helvetica", 8)
    canvas.drawString(
        event_pos(start) + 3, 
        event_height(day, parity) + (25 if parity == "BOTH" else 5),
        event_time,
    )

    # type of class and parallel number
    canvas.drawString(
        event_pos(start) + 5,
        event_height(day, parity) + (35 if parity == "BOTH" else 15),
        f"{EVENT_TYPE[type]}-{parallel_no}",
    )
    canvas.setFont("Helvetica", 10)

    # course name
    canvas.drawString(
        event_pos(start) + 5,
        event_height(day, parity) + (50 if parity == "BOTH" else 30),
        course,
    )


def render(selected_parallel_list: list[Parallel]) -> bytearray:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as file:
        canvas = canv.Canvas(file.name, pagesize=landscape(A4))
        canvas.translate(cm, cm)

        render_day_grid(canvas)

        for parallel in selected_parallel_list:
            for entry in parallel._slots:
                day_of_week, parity, room, start_time, end_time = entry
                render_event(
                    canvas,
                    day_of_week,
                    start_time,
                    end_time,
                    parallel._type,
                    parallel._course,
                    parity,
                    parallel._parallel_no,
                )

        canvas.showPage()
        canvas.save()

        with open(file.name, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        # print(f"Done: {file.name}")

        return base64_pdf