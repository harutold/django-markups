from filters import Library

def render_markup(markup, value, **kwargs):
    Library.dirty()     # Library is not virgin still
    return Library.MARKUPS[markup].render(value, **kwargs)
    
def safe_markups(numerate=False):
    Library.dirty()
    if numerate:
        return [(i, x[0]) for i, x in enumerate(Library.MARKUPS.items()) if x[1].safe]
    return [x[0] for x in Library.MARKUPS.items() if x[1].safe]
    
def all_markups():
    Library.dirty()
    return Library.MARKUPS.keys()
    
def get_markup_num(markup):
    all_markups().index(markup)