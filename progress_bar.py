class ProgressBar:

    hide_coursor = lambda self: print('\033[?25l', end='')
    show_coursor = lambda self: print('\033[?25h', end='')


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
        return self


    def __exit__(self, *args, **kwargs):
        self.show_coursor()

    
    def __getitem__(self, item):
        if item > self.length:
            raise StopIteration()

        line = '{load_char} {_open}{fill}{unfill}{close} {percent}%'.format(
            load_char = self.loading_chars[item % len(self.loading_chars)],
            _open = self.open,
            fill = self.fill * (item - 1) + self.fill_other_first if self.fill_other_first else self.fill,
            unfill = self.unfill * (self.length - item),
            close = self.close,
            percent = item * 100 // self.length
        )

        print(line, end='\r')
        


if __name__ == '__main__':
    import time
    
    with ProgressBar(fill='=', fill_other_first='>', unfill='.') as pb:
        for i in pb:
            time.sleep(.2)
