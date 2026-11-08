"""Local task state machine with dependencies, acceptance evidence and exports."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
from common import configure_console, read_json, report, write_json, write_text

STATES = ('todo', 'doing', 'done')
TRANSITIONS = {'todo': {'doing'}, 'doing': {'todo', 'done'}, 'done': {'todo'}}


def stamp(): return datetime.now(timezone.utc).isoformat(timespec='seconds')


def validate(board):
    if not isinstance(board, dict) or board.get('version') != 1 or not isinstance(board.get('tasks'), list):
        raise ValueError('Invalid board schema')
    tasks = board['tasks']
    ids = [task.get('id') for task in tasks if isinstance(task, dict)]
    if len(ids) != len(tasks) or any(not isinstance(value, str) or not value for value in ids) or len(set(ids)) != len(ids):
        raise ValueError('Task ids must be non-empty and unique')
    mapping = {task['id']: task for task in tasks}
    for task in tasks:
        if task.get('status') not in STATES: raise ValueError('Invalid task status')
        for name in ('title', 'acceptance', 'evidence'):
            if not isinstance(task.get(name), str): raise ValueError('Invalid task text field: ' + name)
        dependencies = task.get('depends_on')
        if not isinstance(dependencies, list) or any(not isinstance(dep, str) or dep not in mapping for dep in dependencies):
            raise ValueError('Dependencies must reference existing tasks')
        if len(set(dependencies)) != len(dependencies): raise ValueError('Duplicate dependency')
    visited, active = set(), set()
    def visit(task_id):
        if task_id in active: raise ValueError('Dependency cycle detected')
        if task_id in visited: return
        active.add(task_id)
        for dep in mapping[task_id]['depends_on']: visit(dep)
        active.remove(task_id); visited.add(task_id)
    for task_id in mapping: visit(task_id)
    for task in tasks:
        if task['status'] == 'done' and (not task['acceptance'].strip() or not task['evidence'].strip()):
            raise ValueError('Completed tasks require acceptance criteria and evidence')
        if task['status'] in ('doing', 'done') and any(mapping[dep]['status'] != 'done' for dep in task['depends_on']):
            raise ValueError('Active/completed task has incomplete dependencies')
    return board


def add(board, title, acceptance, dependencies=()):
    validate(board)
    if not title.strip() or not acceptance.strip(): raise ValueError('Title and acceptance criteria are required')
    if len(board['tasks']) >= 500: raise ValueError('This local board supports at most 500 tasks')
    task_id = f'T{len(board["tasks"]) + 1:03d}'
    if any(task['id'] == task_id for task in board['tasks']): raise ValueError('Generated task id already exists')
    candidate = json.loads(json.dumps(board))
    candidate['tasks'].append({'id': task_id, 'title': title, 'acceptance': acceptance, 'depends_on': list(dependencies),
                               'status': 'todo', 'evidence': '', 'updated_at': stamp()})
    validate(candidate)
    return candidate


def move(board, task_id, status, evidence=''):
    validate(board)
    candidate = json.loads(json.dumps(board))
    mapping = {task['id']: task for task in candidate['tasks']}
    if task_id not in mapping: raise ValueError('Task not found')
    task = mapping[task_id]
    if status not in TRANSITIONS[task['status']]: raise ValueError('Invalid state transition')
    if status == 'todo' and any(task_id in other['depends_on'] and other['status'] in ('doing', 'done') for other in candidate['tasks']):
        raise ValueError('Reopen active/completed dependents first')
    task['status'] = status
    task['evidence'] = evidence.strip() if status == 'done' else ''
    task['updated_at'] = stamp()
    return validate(candidate)


@contextmanager
def board_lock(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = Path(str(path) + '.lock')
    try: descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError: raise ValueError('Board is locked by another writer; inspect stale locks manually') from None
    try:
        os.write(descriptor, str(os.getpid()).encode('ascii'))
        yield
    finally:
        os.close(descriptor)
        lock.unlink(missing_ok=True)


def export(board, output):
    validate(board)
    output = Path(output)
    lines = ['# Codex Task Board', '', '[NB破甲官网](https://nbpojia.lol) · [Telegram 社群](https://t.me/HaoNB_6666)', '']
    columns = []
    for state in STATES:
        cards = []
        lines += ['## ' + state, '']
        for task in board['tasks']:
            if task['status'] != state: continue
            lines += [f"- {'[x]' if state == 'done' else '[ ]'} {task['id']}: {task['title']}", '  - Acceptance: ' + task['acceptance'], '  - Evidence: ' + task['evidence']]
            cards.append('<article class="task"><h3>' + html.escape(task['id'] + ' · ' + task['title']) + '</h3><p>' + html.escape(task['acceptance']) + '</p><p>' + html.escape(task['evidence']) + '</p></article>')
        columns.append('<section class="panel"><h2>' + state + '</h2>' + (''.join(cards) or '<p>No tasks</p>') + '</section>')
    write_text(output / 'board.md', '\n'.join(lines) + '\n')
    write_json(output / 'board.json', board)
    write_text(output / 'board.html', report('Codex Task Board / 编程任务看板',
               {'counts': {state: sum(t['status'] == state for t in board['tasks']) for state in STATES}},
               '<div class="columns">' + ''.join(columns) + '</div>'))


def main():
    configure_console()
    parser = argparse.ArgumentParser(description='Codex task board / 本地任务看板')
    parser.add_argument('--board', type=Path, default=Path('board.json'))
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('init')
    command = commands.add_parser('add'); command.add_argument('title'); command.add_argument('--accept', required=True); command.add_argument('--depends', action='append', default=[])
    command = commands.add_parser('move'); command.add_argument('task'); command.add_argument('status', choices=STATES); command.add_argument('--evidence', default='')
    command = commands.add_parser('export'); command.add_argument('--out', type=Path, default=Path('outputs/board'))
    commands.add_parser('list')
    args = parser.parse_args()
    try:
        if args.command in ('export', 'list'):
            board = validate(read_json(args.board))
            if args.command == 'export': export(board, args.out)
        else:
            with board_lock(args.board):
                if args.command == 'init':
                    if args.board.exists(): raise ValueError('Board already exists; init never overwrites it')
                    board = {'version': 1, 'tasks': []}
                else:
                    board = validate(read_json(args.board))
                    board = add(board, args.title, args.accept, args.depends) if args.command == 'add' else move(board, args.task, args.status, args.evidence)
                write_json(args.board, board)
        print(json.dumps(board, ensure_ascii=False))
    except (ValueError, OSError, RecursionError) as error: parser.exit(2, str(error) + '\n')


if __name__ == '__main__': main()
