from filters import Library

def render_markup(markup, value, **kwargs):
    return Library.MARKUPS[markup].render(value, **kwargs)
    
def safe_markups():
    return [x[0] for x in Library.MARKUPS.items() if x[1].safe]