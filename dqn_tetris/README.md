# Tetris


To initialize:

        - "t = Tetris()" creates tetris game 't'

User functions:

        - t.step() steps fwd in time
        
        - t.print_board() prints board
        
        - t.rotate() rotates current shape
        
        - t.left() moves current shape left
        
        - t.right() moves current shape right


- Currently initializes automatically (for human user), plays through I/O.

        - pass optional sys arg 'width' when calling program (i.e. 'python tetris.py 10')

- I/O instructions: { a:left(), d:right(), w:rotate(), s:step(), p:print_board(), x:print_score(), q:quit() }
