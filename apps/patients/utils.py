from apps.authentication.models import Contact


# The function return dict of day display and his num in db
def get_list_times():
    return dict({
        "1": "ראשון",
        "2": "שני",
        "3": "שלישי",
        "4": "רביעי",
        "5": "חמישי",
        "6": "שישי",
        "7": "שבת",
    })


def get_times_list():
    times = []
    for hour in range(24):
        for minute in range(0, 60, 30):
            times.append('{:02d}:{:02d}:00'.format(hour, minute))
    return times
