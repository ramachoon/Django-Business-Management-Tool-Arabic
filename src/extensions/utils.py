import random

from . import jalali


def jalali_converter(time):
    jmonths = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد',
               'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    time_to_str = f'{time.year},{time.month},{time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonths):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]} '

    return output


def generate_kala_id():
    """
    generate random ID for Kala model.
    """
    number = random.randint(1000000, 9999999)
    return f"AB-{number}"
