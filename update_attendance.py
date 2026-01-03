import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dayflow.settings')
django.setup()

from attendance.models import Attendance
from datetime import time, date

# Get attendance records for January 3, 2026
records = Attendance.objects.filter(date=date(2026, 1, 3))
print(f'Total records: {records.count()}')

# Update checkout times for records
for r in records[:6]:
    if not r.check_out_time:
        r.check_out_time = time(19, 0)
        r.save()
        print(f'Updated {r.employee.user.get_full_name()} - Check In: {r.check_in_time}, Check Out: {r.check_out_time}')
        print(f'  Work Hours: {r.work_hours}, Extra Hours: {r.extra_hours}')
    else:
        print(f'{r.employee.user.get_full_name()} already has checkout time')

print('\nAll records updated!')
