from datetime import datetime

from aiogoogle import Aiogoogle

from app.constants import REPORT_ROW_COUNT, REPORT_COL_COUNT
from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"

now_date_time = datetime.now().strftime(FORMAT)

SPREADSHEET_BODY = {
    'properties': {'title': f'Отчёт на {now_date_time}',
                   'locale': 'ru_RU'},
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': REPORT_ROW_COUNT,
                    'columnCount': REPORT_COL_COUNT
                }
            }
        }
    ]
}

PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}

TABLE_VALUES = [
    ['Отчёт от', now_date_time],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheetid = response['spreadsheetId']
    return (
        spreadsheetid,
        f'https://docs.google.com/spreadsheets/d/{spreadsheetid}'
    )


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=PERMISSIONS_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    for project in projects:
        new_row = [
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description)
        ]
        TABLE_VALUES.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': TABLE_VALUES
    }
    table_cols = max([len(row) for row in TABLE_VALUES])
    if table_cols > REPORT_COL_COUNT or len(TABLE_VALUES) > REPORT_ROW_COUNT:
        raise ValueError()
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:{chr(table_cols + 65)}{len(TABLE_VALUES)}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
