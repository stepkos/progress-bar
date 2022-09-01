class PrintBlocker:

    global print
    oryginal_print = print
    bufor = []

    @staticmethod
    def fake_print(*args, **kwargs):
        PrintBlocker.bufor.append((args, kwargs))

    @staticmethod
    def block():
        global print
        print = PrintBlocker.fake_print

    @staticmethod
    def unlock():
        global print
        print = PrintBlocker.oryginal_print

    @staticmethod
    def get_bufor(clear_bufor = True):
        bufor = PrintBlocker.bufor.copy()
        if clear_bufor:
            PrintBlocker.bufor.clear()
        return bufor


class PrintBlockerContextManager:
    def __init__(self, print_bufor = False, clear_bufor = True):
        self.print_bufor = print_bufor
        self.clear_bufor = clear_bufor

    def __enter__(self):
        PrintBlocker.block()
        return self

    def __exit__(self, *args, **kwargs):
        PrintBlocker.unlock()
        bufor = PrintBlocker.get_bufor(self.clear_bufor)
        if self.print_bufor:
            for _args, _kwargs in bufor:
                print(*_args, **_kwargs)



if __name__ == '__main__':
    print(1)
    with PrintBlockerContextManager(True) as pb:
        print(2)
        print(3)
    print(4)

    print('-'*20)

    print(1)
    PrintBlocker.block()
    print(2)
    print(3)
    PrintBlocker.unlock()
    print(4)
    bufor = PrintBlocker.get_bufor(False)
    for a, k in bufor:
        print(*a, **k)
    print(PrintBlocker.get_bufor())
    print(PrintBlocker.get_bufor())