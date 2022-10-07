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


end_row = 21


def get_jobs_data():
    dbdir = r'F:\PYTHON SCRIPTS\Support Files'
    fname = os.path.join(dbdir, 'MachineTasks.xlsx')
    wb = openpyxl.load_workbook(fname)
    sht = wb['Sheet1']
    # end_row = 16
    part = sht['C2'].value

    jobs_data = []
    job = []
    parts = [part]
    for i in range(2, end_row):
        if int(sht['G' + str(i)].value) == 3:
            machine_id = randint(0, 1)
        else:
            machine_id = int(sht['G' + str(i)].value)
        processing_time = int(sht['H' + str(i)].value)
        processing_time = processing_time + (int(sht['B' + str(i)].value) * int(sht['I' + str(i)].value))
        task = (machine_id, processing_time)
        if sht['C' + str(i)].value == part:
            job.append(task)
        else:
            jobs_data.append(job)
            job = [task]
            part = sht['C' + str(i)].value
        if part not in parts:
            parts.append(part)
    jobs_data.append(job)
    return jobs_data, parts


def get_tasks():
    """Minimal jobshop problem."""
    # Data.
    jobs_data = [  # task = (machine_id, processing_time).
        [(0, 3), (1, 2), (2, 2)],  # Job0
        [(0, 2), (2, 1), (1, 4)],  # Job1
        [(1, 4), (2, 3)]  # Job2
    ]
    jobs_data, parts = get_jobs_data()

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
    return assigned_jobs, solver, all_machines, parts


def main():
    assigned_jobs_f, solver_f, all_machines_f, parts_f = get_tasks()
    for i in range(0, 1):
        assigned_jobs, solver, all_machines, parts = get_tasks()
        if solver.ObjectiveValue() < solver_f.ObjectiveValue():
            assigned_jobs_f, solver_f, all_machines_f, parts_f = assigned_jobs, solver, all_machines, parts
    assigned_jobs, solver, all_machines, parts = assigned_jobs_f, solver_f, all_machines_f, parts_f
    hours_all = int(solver.ObjectiveValue() * 5)

    page_width = 300 * 8
    page_height = 300 * 10
    img_final = Image.new("RGBA", (page_width, page_height), color="white")
    img_draw = ImageDraw.Draw(img_final)
    font_path = r'C:\Windows\Fonts\calibrib.ttf'
    font = ImageFont.truetype(font_path, 15)

    img = Image.new("RGBA", (hours_all, 200), color="white")
    im_draw = ImageDraw.Draw(img)

    #  use the color_chart() thing to pick colors
    job_colors = ['yellow', 'beige', 'aqua', 'cyan', 'lightcoral', 'plum', 'lime', 'lightskyblue', 'orange', 'lightgray']

    #  Page Template
    y_s = 0
    y_f = page_height
    for i in range(0, 8):
        x_s = i * 300
        x_f = x_s + 300
        img_draw.rectangle([(x_s, y_s), (x_f, y_f)], fill='white', outline='black')

    #  Draw full bar
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

    x_s = 0
    x_f = x_s + page_width
    y_s = 33
    y_f = y_s + 200

    print(img.size)
    if img.size[0] > page_width:
        crop = img.crop((0, 0, page_width, 200))
        img_final.paste(crop, (x_s, y_s, x_f, y_f))
    else:
        crop = img.crop((0, 0, img.size[0], 200))
        img_final.paste(crop, (x_s, y_s, img.size[0], y_f))
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

    job_colors = ['yellow', 'blue', 'cyan', 'red', 'purple', 'green', 'gold', 'orange']
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
