import copy
import tempfile
import unittest
from pathlib import Path
import main

class BoardTests(unittest.TestCase):
    def board(self):return main.add({'version':1,'tasks':[]},'Implement','Tests pass')
    def done(self):return main.move(main.move(self.board(),'T001','doing'),'T001','done','Test run 12 passed')
    def test_complete_requires_evidence(self):
        board=main.move(self.board(),'T001','doing')
        with self.assertRaises(ValueError):main.move(board,'T001','done')
        self.assertEqual(self.done()['tasks'][0]['status'],'done')
    def test_transition_and_immutable_input(self):
        board=self.board()
        with self.assertRaises(ValueError):main.move(board,'T001','done','evidence')
        self.assertEqual(board['tasks'][0]['status'],'todo')
    def test_dependency_gate(self):
        board=main.add(self.board(),'Ship','Release exists',['T001'])
        with self.assertRaises(ValueError):main.move(board,'T002','doing')
        board=main.add(self.done(),'Ship','Release exists',['T001'])
        self.assertEqual(main.move(board,'T002','doing')['tasks'][1]['status'],'doing')
    def test_cycles_and_missing_ids(self):
        with self.assertRaises(ValueError):main.add(self.board(),'X','Y',['missing'])
        board=self.board();board['tasks'][0]['depends_on']=['T001']
        with self.assertRaises(ValueError):main.validate(board)
    def test_reopen_active_dependency_blocked(self):
        board=main.move(main.add(self.done(),'Ship','Release exists',['T001']),'T002','doing')
        with self.assertRaises(ValueError):main.move(board,'T001','todo')
    def test_lock_contention_and_cleanup(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'board.json'
            with main.board_lock(p):
                with self.assertRaises(ValueError):
                    with main.board_lock(p):pass
            self.assertFalse(Path(str(p)+'.lock').exists())
    def test_exports_escape_html(self):
        with tempfile.TemporaryDirectory() as temp:
            board=main.add({'version':1,'tasks':[]},'<script>','Test');main.export(board,temp)
            content=(Path(temp)/'board.html').read_text(encoding='utf-8')
            self.assertNotIn('<script>',content);self.assertIn('&lt;script&gt;',content)
            self.assertTrue((Path(temp)/'board.json').exists())
