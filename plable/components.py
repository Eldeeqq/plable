from datetime import datetime


def parse_slot(slot):
    return (slot.day(), slot.parity(), slot.room(), slot.startTime(), slot.endTime())


def overlap(a, b):
    """
    Checks whether two events overlap
    """
    day_a, parity_a, room_a, start_a, end_a = a
    day_b, parity_b, room_b, start_b, end_b = b
    (5, "BOTH", "TK:PU1", "09:15:00", "10:45:00")
    if day_a != day_b:
        return False
    start_a, start_b, end_a, end_b = map(lambda x: datetime.strptime(x, "%H:%M:%S"), [start_a, start_b, end_a, end_b])
    # if times overlap -> collision
    if (start_a <= start_b <= end_a) or (start_b <= start_a <= end_b):
        # the only exception is with 'ODD' 'EVEN' combination:
        return False if set([parity_a, parity_b]) == set(["EVEN", "ODD"]) else True


class Parallel:
    def __init__(
        self,
        course,
        course_fullname,
        semester,
        type,
        parallel_no,
        occupied,
        capacity,
        teachers: set,
        slots: list,
    ) -> None:
        self._course = course
        self._course_fullname = course_fullname
        self._semester = semester
        self._parallel_no = parallel_no
        self._occupied = occupied
        self._capacity = capacity
        self._teachers = teachers
        self._slots = slots
        self._type = type

    def __repr__(self) -> str:
        return f"<Parallel {self._parallel_no} [{self._course}|{self._type}]>"

    def __str__(self) -> str:
        return f"{self._course}/{self._type}/{self._parallel_no}"

    def collision_free(self, other):
        if not isinstance(other, Parallel):
            raise Exception("Unsupported binary operation")

        # The courses are the same
        if self._course == other._course:
            if self._parallel_no == other._parallel_no:
                return True

            # same course, same type of parallel -> collision
            elif self._type == other._type:
                return False

        # todo check time collisions
        for s_slot in self._slots:
            for o_slot in other._slots:
                if overlap(s_slot, o_slot):
                    # print( s_slot, o_slot, sep='\n', end='\n'+ '#'*20+'\n',)
                    return False
        return True

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Parallel):
            return False
        return self._course == o._course and self._parallel_no == o._parallel_no
