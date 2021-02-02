from h2o_wave import main, app, Q
from pages.technical_analysis_page import show_technical_analysis


@app('/')
async def serve(q: Q):
    route = q.args['#']
    q.page.drop()
    if route == 'analysis':
        await show_technical_analysis(q)
    else:
        await show_technical_analysis(q)
