
# The function return dict of day display and his num in db
def get_days_list():
    d = dict({
        "1": "ראשון",
        "2": "שני",
        "3": "שלישי",
        "4": "רביעי",
        "5": "חמישי",
        "6": "שישי",
        "7": "שבת"
    })
    # l = [(key, value, "") for (key, value) in d.items()]
    # l[1] = ('2', 'שני', 'selected')
    return [(key, value) for (key, value) in d.items()]

def get_times_list():
    times = []
    for hour in range(24):
        for minute in range(0, 60, 30):
            times.append('{:02d}:{:02d}:00'.format(hour, minute))
    times = [("time",value) for value in times]
    return times
