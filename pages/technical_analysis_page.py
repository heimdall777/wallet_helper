from datetime import datetime

from h2o_wave import ui, Q

from analysis.mpi import MoneyFlowIndex
from analysis.rsi import RelativeStrengthIndex
from pages.commons.analysis_types import analysis_types
from pages.commons.common import global_nav
from pages.commons.input_types import input_types
from services.upload_service import UploadService
from utils.parser import parse_df_to_records
from widgets.df_table import DataFrameTable


async def show_technical_analysis(q: Q):
    q.page['meta'] = ui.meta_card(box='', layouts=[
        ui.layout(
            breakpoint='xl',
            width='1200px',
            zones=[
                ui.zone('header'),
                # ui.zone('title'),
                ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone('sidebar', size='25%'),
                    ui.zone('content', size='75%'),
                ]),
                ui.zone('footer'),
            ]
        )
    ])

    q.page['header'] = ui.header_card(box='header', title='Wallet App', subtitle='Technical Analysis',
                                      nav=global_nav)

    q.page['process_panel'] = ui.form_card(
        box=ui.box('sidebar', height='520', order=2),
        items=[]
    )

    if q.args.calculate or q.args.file_upload:
        upload_service = UploadService()
        df = await upload_service.upload(q)

        records = await parse_df_to_records(df)
        df_table = DataFrameTable()

        q.page['data_table'] = ui.form_card(box='content', items=[
            df_table.show(records)
        ])

        await process_mfi(df, q)
        await process_rsi(df, q)

    process_panel = q.page['process_panel']
    await __show_process_input_panel(process_panel, q)

    await q.page.save()


async def process_mfi(df, q):
    if 'MFI' in q.args.analysis_types:
        mfi = MoneyFlowIndex(df)
        result_mfi_df = mfi.calculate()
        await mfi.show_mpi(q, result_mfi_df)
        await mfi.show_close_price_plot_with_signals(q, result_mfi_df)


async def process_rsi(df, q):
    if 'RSI' in q.args.analysis_types:
        rsi = RelativeStrengthIndex(df)
        result_rsi_df = rsi.calculate()
        await rsi.show_rsi(q, result_rsi_df)


async def __show_process_input_panel(process_panel, q):
    if q.args.input_type == 'F':
        process_panel.items = [
            ui.label(label='Ticker:'),
            ui.textbox(name='ticker', value=q.args.ticker, required=True),
            ui.picker(name='analysis_types', label='Select technical analysis', values=q.args.analysis_types,
                      choices=analysis_types),
            ui.choice_group(name='input_type', label='Pick one', required=True, choices=input_types,
                            value=q.args.input_type, trigger=True),
            ui.file_upload(name='file_upload', label='Calculate', multiple=False, file_extensions=['csv']
                           , height='180px'),
        ]
    elif q.args.input_type in ['Y', 'S']:
        process_panel.items = [
            ui.label(label='Ticker:'),
            ui.textbox(name='ticker', value=q.args.ticker, required=True),
            ui.label(label='Start:'),
            ui.date_picker(name='start_date', label='', value=q.args.start_date),
            ui.label(label='End:'),
            ui.date_picker(name='end_date', label='', value=q.args.end_date),
            ui.picker(name='analysis_types', label='Select technical analysis', values=q.args.analysis_types,
                      choices=analysis_types),
            ui.choice_group(name='input_type', label='Pick one', required=True, choices=input_types,
                            value=q.args.input_type, trigger=True),
            ui.button(name='calculate', label='Calculate', primary=True),
        ]
    else:
        process_panel.items = [
            ui.label(label='Ticker:'),
            ui.textbox(name='ticker', required=True),
            ui.label(label='Start:'),
            ui.date_picker(name='start_date', label='', value=datetime.today().strftime('%Y-%m-%d')),
            ui.label(label='End:'),
            ui.date_picker(name='end_date', label='', value=datetime.today().strftime('%Y-%m-%d')),
            ui.picker(name='analysis_types', label='Select technical analysis', values=[],
                      choices=analysis_types),
            ui.choice_group(name='input_type', label='Pick one', required=True, choices=input_types, trigger=True),
            ui.button(name='calculate', label='Calculate', primary=True),
        ]
