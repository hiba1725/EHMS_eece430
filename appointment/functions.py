def find_available_slots(appts):
    """
    A function that finds available time slots for a particular doctor and day
    input: QuerySet of appointments on day X with doctor Y
    output: list of available time slots on day X with doctor Y
    """

    N = 10

    slots = {}
    for i in range(0,N):
        slots[i] = False
    for appt in appts:
        appt_slot = appt.slot
        slots[appt_slot] = True


    available_slots = []
    for i in range(0,N):
        if(not slots[i]):
            available_slots.append(f'{8+i}:00-{9+i}:00')
    
    return available_slots

def encode_slot(slot):
    i = 0
    s = ""
    while(slot[i]!=':'):
        s = s + slot[i]
        i = i + 1
    start_time = int(s)
    slot = start_time - 8
    return slot
    
            