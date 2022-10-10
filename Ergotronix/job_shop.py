"""Minimal jobshop example."""
import collections
from ortools.sat.python import cp_model
import openpyxl
import os
from random import randint
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageColor
import math
import airtable_project
from string import ascii_uppercase as alpha_cols

end_row = 46
num_iterations = 20


def color_chart():
    c = ImageColor.colormap
    n = len(c)
    cols = 4
    rows = ((n - 1) // cols) + 1
    cellHeight = 30
    cellWidth = 170
    imgHeight = cellHeight * rows
    imgWidth = cellWidth * cols
    i = Image.new("RGB", (imgWidth, imgHeight), (0, 0, 0))
    a = ImageDraw.Draw(i)
    for idx, name in enumerate(c):
        y0 = cellHeight * (idx // cols)
        y1 = y0 + cellHeight
        x0 = cellWidth * (idx % cols)
        x1 = x0 + (cellWidth / 4)
        a.rectangle([x0, y0, x1, y1], fill=name, outline='black')
        a.text((x1 + 1, y0 + 10), name, fill='white')
    i.show()


def get_jobs_data():
    #  dbdir = r'F:\PYTHON SCRIPTS\Support Files'  #  WORK
    dbdir = r'C:\Users\Sad_Matt\Desktop\Python\Ergotronix\job_shop'  # HOME
    fname = os.path.join(dbdir, 'MachineTasks.xlsx')
    wb = openpyxl.load_workbook(fname)
    sht = wb['Sheet1']
    # end_row = 16
    part = sht['C2'].value
    attrs = []
    rows = []
    for i in range(0, 11):
        attrs.append(sht[f'{alpha_cols[i]}1'].value)
    for i in range(2, end_row):
        row = []
        for j in range(0, 11):
            row.append(sht[f'{alpha_cols[j]}{i}'].value)
        rows.append(row)
    jobs = airtable_project.Project4(attrs, rows)
    jobs = [item for item in jobs.items]
    jobs_data = []
    parts_info = [jobs[0]]
    part = jobs[0].part
    parts = []
    work = []
    for job in jobs:
        machine_id = int(job.machine_id)
        if machine_id == 3:
            machine_id = randint(0, 1)
        processing_time = int(int(job.set_up_time) + int(job.qty) * int(job.processing_time))
        task = (machine_id, processing_time)
        if job.part == part:
            work.append(task)
        else:
            jobs_data.append(work)
            work = [task]
            parts.append(part)
            part = job.part
            parts_info.append(job)
    jobs_data.append(work)
    return jobs_data, parts_info


def get_tasks():
    """Minimal jobshop problem."""
    # Data.
    jobs_data = [  # task = (machine_id, processing_time).
        [(0, 3), (1, 2), (2, 2)],  # Job0
        [(0, 2), (2, 1), (1, 4)],  # Job1
        [(1, 4), (2, 3)]  # Job2
    ]
    jobs_data, parts_info = get_jobs_data()

    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)
    # Computes horizon dynamically as the sum of all durations.
    horizon = sum(task[1] for job in jobs_data for task in job)

    # Create the model.
    model = cp_model.CpModel()

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval')
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index duration')

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task[0]
            duration = task[1]
            suffix = '_%i_%i' % (job_id, task_id)
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
            all_tasks[job_id, task_id] = task_type(start=start_var,
                                                   end=end_var,
                                                   interval=interval_var)
            machine_to_intervals[machine].append(interval_var)

    # Create and add disjunctive constraints.
    for machine in all_machines:
        model.AddNoOverlap(machine_to_intervals[machine])

    # Precedences inside a job.
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id +
                                1].start >= all_tasks[job_id, task_id].end)

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Create one list of assigned tasks per machine.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(start=solver.Value(
                        all_tasks[job_id, task_id].start),
                        job=job_id,
                        index=task_id,
                        duration=task[1]))

        for machine in all_machines:
            assigned_jobs[machine].sort()
    else:
        pass
    return assigned_jobs, solver, all_machines, parts_info


def main():
    page_width = 300 * 10
    page_height = 300 * 8
    hour_width = int(page_width / 8)
    minute = int(hour_width / 60)
    assigned_jobs_f, solver_f, all_machines_f, parts_info_f = get_tasks()
    day_width = 7 * hour_width
    for i in range(0, num_iterations):
        assigned_jobs, solver, all_machines, parts_info = get_tasks()
        if solver.ObjectiveValue() < solver_f.ObjectiveValue():
            assigned_jobs_f, solver_f, all_machines_f, parts_info_f = assigned_jobs, solver, all_machines, parts_info
    assigned_jobs, solver, all_machines, parts_info = assigned_jobs_f, solver_f, all_machines_f, parts_info_f
    hours_all = int(solver.ObjectiveValue() * minute)

    img_final = Image.new("RGBA", (page_width, page_height), color="white")
    img_draw = ImageDraw.Draw(img_final)
    font_path = r'C:\Windows\Fonts\calibrib.ttf'
    font = ImageFont.truetype(font_path, 25)
    font_big = ImageFont.truetype(font_path, 50)

    img = Image.new("RGBA", (hours_all, 200), color="white")
    im_draw = ImageDraw.Draw(img)

    #  use the color_chart() thing to pick colors
    job_colors = ['red', 'steelblue', 'olivedrab', 'darkorchid', 'mediumturquoise', 'darkorange', 'darkgoldenrod',
                  'mediumslateblue', 'lawngreen', 'mediumvioletred', 'sienna']

    #  Draw full bar
    for machine in all_machines:
        y_s = 66 * machine + machine
        y_f = y_s + 66
        im_draw.rectangle([(0, y_s), (hours_all, y_f)], fill='white', outline='black')
        tasks = assigned_jobs[machine]
        print(f"                 Machine: {machine}")
        for task in tasks:
            x_s = int(task.start * minute)
            x_f = int(task.duration * minute + x_s)
            x_text = int(x_s + ((x_f - x_s) / 2))
            y_text_job = y_f - 33 - 10
            y_text_task = y_f - 33 + 10
            anchor = 'mm'
            x_split = int((x_s / day_width) + 1) * day_width
            if x_s < x_split < x_f:
                if x_text < x_split:
                    x_text = int(x_s + ((x_split - x_s) / 2))
                else:
                    x_text = int(x_split + ((x_f - x_split) / 2))
            im_draw.rectangle([(x_s, y_s), (x_f, y_f)], fill=job_colors[task.job % len(job_colors)], outline='black')
            im_draw.text((x_text, y_text_job), f'{parts_info[task.job].part}', font=font, anchor=anchor, fill='black',
                         stroke_fill='white', stroke_width=3)
            im_draw.text((x_text, y_text_task), f'Task: {task.index}', font=font, anchor=anchor, fill='black',
                         stroke_fill='white', stroke_width=3)
        print("-------------------------------------------------")
    # img.show()
    page_top = (int(img.size[0] / (page_width - hour_width)) + 1) * 100 + (
        int(img.size[0] / (page_width - hour_width))) * 200 + 200

    #  Page Template
    y_s = 0
    y_f = page_top
    for i in range(0, 8):
        x_s = i * hour_width
        x_f = x_s + hour_width
        if i % 2 == 0:
            img_draw.rectangle([(x_s, y_s), (x_f, y_f)], fill='lightgray')  # , outline='black')
        else:
            img_draw.rectangle([(x_s, y_s), (x_f, y_f)], fill='white')  # , outline='black')

    #  Crop Full Bar Onto Page
    for i in range(0, int(img.size[0] / (page_width - hour_width))):
        x_s = i * (page_width - hour_width)
        x_f = x_s + (page_width - hour_width)
        y_s = (i + 1) * 100 + i * 200
        y_f = y_s + 200
        crop = img.crop((x_s, 0, x_f, 200))
        img_draw.rectangle([(0, y_s - 5), (page_width, y_f + 5)], fill='black', outline='black')
        img_draw.rectangle([(0, y_s), (page_width, y_f)], fill='white', outline='black')
        img_draw.text((0.5 * hour_width, y_s + 100), f'DAY: {i + 1}', font=font_big, anchor="mm", fill='black')
        img_draw.text((hour_width - 50, y_s + 33), f'VMX30', font=font, anchor="mm", fill='black')
        img_draw.text((hour_width - 50, y_s + 100), f' VM30', font=font, anchor="mm", fill='black')
        img_draw.text((hour_width - 50, y_s + 166), f'LATHE', font=font, anchor="mm", fill='black')
        img_final.paste(crop, (hour_width, y_s, page_width, y_f))

    x_s = int(img.size[0] / (page_width - hour_width)) * (page_width - hour_width)
    x_f = img.size[0]
    y_s = (int(img.size[0] / (page_width - hour_width)) + 1) * 100 + (
        int(img.size[0] / (page_width - hour_width))) * 200
    y_f = y_s + 200
    crop = img.crop((x_s, 0, x_f, 200))
    img_draw.rectangle([(0, y_s - 5), (page_width, y_f + 5)], fill='black', outline='black')
    img_draw.rectangle([(0, y_s), (page_width, y_f)], fill='white', outline='black')
    img_draw.text((0.5 * hour_width, y_s + 100), f'DAY: {int(img.size[0] / (page_width - hour_width)) + 1}', 
                  font=font_big, anchor="mm", fill='black')
    img_draw.text((hour_width - 50, y_s + 33), f'VMX30', font=font, anchor="mm", fill='black')
    img_draw.text((hour_width - 50, y_s + 100), f' VM30', font=font, anchor="mm", fill='black')
    img_draw.text((hour_width - 50, y_s + 166), f'LATHE', font=font, anchor="mm", fill='black')
    img_final.paste(crop, (hour_width, y_s, x_f - x_s + hour_width, y_f))

    img_draw.rectangle([(0, page_top), (page_width, page_top + 5)], fill='black', outline='black')

    font = ImageFont.truetype(font_path, 40)
    y_task_spacing = 100
    x_task_spacing = 200
    machine_arr = ['VMX30', 'VM30', 'LATHE']
    y_s = page_top + 50
    for machine in all_machines:
        x_s = hour_width
        img_draw.text((0.5 * hour_width,
                       y_s + 0.5 * y_task_spacing),
                      machine_arr[machine], font=font_big, anchor='mm', fill='black')
        tasks = assigned_jobs[machine]
        for task in tasks:
            x_f = int(task.start * minute)
            y_f = int(task.duration * minute + x_s)
            img_draw.rectangle([(x_s - int(0.2 * x_task_spacing), y_s - int(0.2 * y_task_spacing)),
                                (x_s + int(1.2 * x_task_spacing), y_s + int(1.2 * y_task_spacing))],
                               fill=job_colors[task.job % len(job_colors)], outline='black')
            img_draw.text((x_s + 0.5 * x_task_spacing, y_s + int(0.2 * y_task_spacing)),
                          f'{parts_info[task.job].part}', font=font, anchor='mm', fill='black',
                          stroke_fill='white', stroke_width=3)
            img_draw.text((x_s + 0.5 * x_task_spacing, y_s + int(0.5 * y_task_spacing)),
                          f'{parts_info[task.job].Customer}', font=font, anchor='mm', fill='black',
                          stroke_fill='white', stroke_width=3)
            img_draw.text((x_s + 0.5 * x_task_spacing, y_s + int(0.8 * y_task_spacing)),
                          f'{parts_info[task.job].Sub_Assembly}', font=font, anchor='mm', fill='black',
                          stroke_fill='white', stroke_width=3)
            if x_s + 2 * x_task_spacing < page_width:
                x_s = x_s + 1.5 * x_task_spacing
            else:
                y_s = y_s + 1.5 * y_task_spacing
                x_s = hour_width
        y_s = y_s + 1.5 * y_task_spacing
        img_draw.rectangle([(0, y_s - int(0.4*y_task_spacing)),
                            (page_width, y_s - int(0.4*y_task_spacing) + 5)],
                           fill='black', outline='black')



    r'''
    img_draw.rectangle([(hour_width - 3, page_top), (hour_width + 2, page_height)],
                       fill='black', outline='black')
    for machine in all_machines:
        img_draw.text((x_s + int(0.5*x_task_spacing), page_top + 75), machine_arr[machine], 
                      font=font_big, anchor='mm', fill='black')
        y_s = page_top + 150
        tasks = assigned_jobs[machine]
        for task in tasks:
            x_f = int(task.start * minute)
            y_f = int(task.duration * minute + x_s)
            img_draw.rectangle([(x_s, y_s), (x_s + x_task_spacing, y_s + int(0.8 * y_task_spacing))],
                               fill=job_colors[task.job % len(job_colors)], outline='black')
            img_draw.text((x_s + 0.5 * x_task_spacing, y_s + int(0.25 * y_task_spacing)),
                          f'{parts_info[task.job].part}', font=font, anchor='mm', fill='black',
                          stroke_fill='white', stroke_width=3)
            img_draw.text((x_s + 0.5 * x_task_spacing, y_s + int(0.5 * y_task_spacing)),
                          f'{parts_info[task.job].Customer}', font=font, anchor='mm', fill='black',
                          stroke_fill='white', stroke_width=3)
            img_draw.text((x_s + 0.5 * x_task_spacing, y_s + int(0.75 * y_task_spacing)),
                          f'{parts_info[task.job].Sub_Assembly}', font=font, anchor='mm', fill='black',
                          stroke_fill='white', stroke_width=3)
            if y_s + 2 * y_task_spacing < page_height:
                y_s = y_s + y_task_spacing
            else:
                y_s = page_top + 1.5 * y_task_spacing
                x_s = x_s + 1.5 * x_task_spacing
        img_draw.rectangle(
            [(x_s + 1.25 * x_task_spacing - 3, page_top), (x_s + 1.25 * x_task_spacing + 2, page_height)], fill='black',
            outline='black')
        x_s = x_s + 1.5 * x_task_spacing
    '''


    img_final.show()


def main1():
    """Minimal jobshop problem."""
    # Data.
    jobs_data = [  # task = (machine_id, processing_time).
        [(0, 3), (1, 2), (2, 2)],  # Job0
        [(0, 2), (2, 1), (1, 4)],  # Job1
        [(1, 4), (2, 3)]  # Job2
    ]
    jobs_data, parts = get_jobs_data()
    for job in jobs_data:
        print(job)

    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)
    # Computes horizon dynamically as the sum of all durations.
    horizon = sum(task[1] for job in jobs_data for task in job)

    # Create the model.
    model = cp_model.CpModel()

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval')
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index duration')

    # Creates job intervals and add to the corresponding machine lists.
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task[0]
            duration = task[1]
            suffix = '_%i_%i' % (job_id, task_id)
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
            all_tasks[job_id, task_id] = task_type(start=start_var,
                                                   end=end_var,
                                                   interval=interval_var)
            machine_to_intervals[machine].append(interval_var)

    # Create and add disjunctive constraints.
    for machine in all_machines:
        model.AddNoOverlap(machine_to_intervals[machine])

    # Precedences inside a job.
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id +
                                1].start >= all_tasks[job_id, task_id].end)

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Solution:')
        # Create one list of assigned tasks per machine.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(start=solver.Value(
                        all_tasks[job_id, task_id].start),
                        job=job_id,
                        index=task_id,
                        duration=task[1]))

        # Create per machine output lines.
        output = ''
        for machine in all_machines:
            # Sort by starting time.
            assigned_jobs[machine].sort()
            sol_line_tasks = 'Machine ' + str(machine) + ': '
            sol_line = '           '

            for assigned_task in assigned_jobs[machine]:
                name = 'job_%i_task_%i' % (assigned_task.job,
                                           assigned_task.index)
                # Add spaces to output to align columns.
                sol_line_tasks += '%-15s' % name

                start = assigned_task.start
                duration = assigned_task.duration
                sol_tmp = '[%i,%i]' % (start, start + duration)
                # Add spaces to output to align columns.
                sol_line += '%-15s' % sol_tmp

            sol_line += '\n'
            sol_line_tasks += '\n'
            output += sol_line_tasks
            output += sol_line

        # Finally print the solution found.
        print(f'Optimal Schedule Length: {solver.ObjectiveValue()}')
        print(output)
    else:
        print('No solution found.')

    # Statistics.
    print('\nStatistics')
    print('  - conflicts: %i' % solver.NumConflicts())
    print('  - branches : %i' % solver.NumBranches())
    print('  - wall time: %f s' % solver.WallTime())
    print("===============================================================================")

    hours_all = int(solver.ObjectiveValue() * 5)

    page_width = 300 * 8
    page_height = 300 * 10
    img_final = Image.new("RGBA", (page_width, page_height), color="white")
    img_draw = ImageDraw.Draw(img_final)
    font_path = r'C:\Windows\Fonts\calibrib.ttf'
    font = ImageFont.truetype(font_path, 15)

    img = Image.new("RGBA", (hours_all, 200), color="white")
    im_draw = ImageDraw.Draw(img)

    job_colors = ['red', 'steelblue', 'olivedrab', 'darkorchid', 'mediumturquoise', 'darkorange', 'darkgoldenrod',
                  'mediumslateblue', 'lawngreen', 'mediumvioletred', 'sienna']
    for machine in all_machines:
        y_s = 66 * machine + machine
        y_f = y_s + 66
        im_draw.rectangle([(0, y_s), (hours_all, y_f)], fill='white', outline='black')
        tasks = assigned_jobs[machine]
        print(f"                 Machine: {machine}")
        for task in tasks:
            x_s = int(task.start * 5)
            x_f = int(task.duration * 5 + x_s)
            x_text = int(x_s + ((x_f - x_s) / 2))
            y_text_job = y_f - 33 - 10
            y_text_task = y_f - 33 + 10
            print(f'job: {parts[task.job]} | task: {task.index}')
            print(f'[{task.start},{task.start + task.duration}]')
            print("- - - - - - - - - - - - - - -")
            im_draw.rectangle([(x_s, y_s), (x_f, y_f)], fill=job_colors[task.job % len(job_colors)], outline='black')
            im_draw.text((x_text, y_text_job), f'Part:{parts[task.job]}', font=font, anchor="mm", fill='black')
            im_draw.text((x_text, y_text_task), f'Task: {task.index}', font=font, anchor="mm", fill='black')
        print("-------------------------------------------------")
    img.show()


if __name__ == '__main__':
    main()
