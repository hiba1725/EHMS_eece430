def find_available_slots(appts):
    """
    A function that finds available time slots for a particular doctor and day
    input: QuerySet of appointments on day X with doctor Y
    output: list of available time slots on day X with doctor Y
    """

    slots = {}
    for i in range(0,8):
        slots[i] = False
    for appt in appts:
        appt_slot = appt.slot
        slots[appt_slot] = True


    available_slots = []
    for i in range(0,8):
        if(not slots[i]):
            available_slots.append(slots[i])
    
    return available_slots
    
            