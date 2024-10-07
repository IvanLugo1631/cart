from datetime import time, timedelta, datetime
import re

def convert_string_to_time_list(schedule_string):
    pattern = r'\(time\((\d+),\s*(\d+)\),\s*time\((\d+),\s*(\d+)\)\)'
    matches = re.findall(pattern, schedule_string)
    
    time_list = []
    
    for match in matches:
        start_hour, start_minute, end_hour, end_minute = map(int, match)
        time_list.append((time(start_hour, start_minute), time(end_hour, end_minute)))
    return time_list

def verify_time_range(schedule_list, work_end):
    if not schedule_list:
        print("Schedule list is empty.")
        return False
    last_meeting_start, last_meeting_end = schedule_list[-1]
    if last_meeting_end <= work_end:
        return True
    else:
        return False

def verify_meeting_duration(meeting_duration):
    try:
        hours = float(meeting_duration)
        
        if hours % 0.5 != 0:
            raise ValueError
        meeting_duration = timedelta(hours=hours)
        return meeting_duration

    except ValueError:
        print("Invalid input. Please specify the meeting duration in hours (e.g., 1, 1.5, 2) with deltas of 30 minutes.")
        return None

def find_available_slots(schedule_list, meeting_duration):
    work_start = time(9, 0)
    work_end = time(17, 0)

    meeting_duration_timedelta = verify_meeting_duration(meeting_duration)
    if not meeting_duration_timedelta:
        return

    available_slots = []

    if schedule_list:
        first_meeting_start = schedule_list[0][0]
        if first_meeting_start > work_start:
            available_slots.append((work_start, first_meeting_start))

    for i in range(len(schedule_list) - 1):
        end_current_meeting = schedule_list[i][1]
        start_next_meeting = schedule_list[i + 1][0]

        if start_next_meeting > end_current_meeting:
            available_slots.append((end_current_meeting, start_next_meeting))

    if schedule_list:
        last_meeting_end = schedule_list[-1][1]
        if last_meeting_end < work_end:
            available_slots.append((last_meeting_end, work_end))

    available_time_slots = []
    for start, end in available_slots:
        duration = (datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(), start)).total_seconds() / 60 
        if duration >= meeting_duration_timedelta.total_seconds() / 60:
            available_time_slots.append((start, end))

    print("Available slots for scheduling meetings:")
    for start, end in available_time_slots:
        print(f"From {start} to {end}")

    return available_time_slots

def main():
    while True:
        schedule_input = input("Insert schedule list (e.g., [(time(9, 0), time(10, 30)), ...]): \n")
        schedule_list = convert_string_to_time_list(schedule_input)
        schedule_list.sort(key=lambda x: x[0])
        print("Sorted schedule list: \n", schedule_list)

        work_end = time(17, 0)
        is_within_range = verify_time_range(schedule_list, work_end)

        while True:
            meeting_duration = input("Specify meeting duration in hours (e.g., '1', '1.5', '2') with deltas of 30 minutes: \n")
            meeting_duration_timedelta = verify_meeting_duration(meeting_duration)

            if meeting_duration_timedelta:
                break
        
        print("Finding available hours...")
        find_available_slots(schedule_list, meeting_duration)

        another_schedule = input("Do you want to verify another schedule list? (yes/no): ").strip().lower()
        if another_schedule != 'yes':
            break

    return

if __name__ == "__main__":
    main()