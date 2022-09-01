from print_blocker import PrintBlocker


class ProgressBar:

    hide_coursor = lambda self: print('\033[?25l', end='')
    show_coursor = lambda self: print('\033[?25h', end='')
    block_print = lambda self: PrintBlocker.block(globals())
    unlock_print = lambda self: PrintBlocker.unlock(globals())
    display_print_bufor = lambda self: PrintBlocker.print_bufor()


    def __init__(self, length: int = 20,
            _open: str = '[', close: str = ']',
            fill: str = '#', fill_other_first: str = '',
            unfill: str = ' ', loading_chars: str = r'-\|/'):

        self.length = length
        self.open, self.close = _open, close
        self.fill, self.unfill = fill, unfill
        self.fill_other_first = fill_other_first
        self.loading_chars = loading_chars

    
    def __enter__(self):
        self.hide_coursor()
        self.block_print()
        return self


    def __exit__(self, *args, **kwargs):
        self.show_coursor()
        self.unlock_print()
        self.display_print_bufor()

    
    def __getitem__(self, item):
        if item > self.length:
            self.unlock_print()
            print()
            self.block_print()
            raise StopIteration()

        line = '{load_char} {_open}{fill}{unfill}{close} {percent}%'.format(
            load_char = self.loading_chars[item % len(self.loading_chars)],
            _open = self.open,
            fill = self.fill * (item - 1) + self.fill_other_first if self.fill_other_first else self.fill,
            unfill = self.unfill * (self.length - item),
            close = self.close,
            percent = item * 100 // self.length
        )

        self.unlock_print()
        print(line, end='\r')
        self.block_print()
        


if __name__ == '__main__':
    import time
    
    with ProgressBar(fill='=', fill_other_first='>', unfill='.') as pb:
        print('Hello')
        for i in pb:
            print('Im interapting now!')
            time.sleep(.2)
