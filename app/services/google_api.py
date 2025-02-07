from datetime import datetime

from aiogoogle import Aiogoogle

from app.constants import (
    REPORT_ROW_COUNT, REPORT_COL_COUNT, FORMAT, UNICODE_START_CHAR_NUM,
    TABLE_VALUES_DATE_ROW_INDEX, TABLE_VALUES_DATE_COL_INDEX
)
from app.core.config import settings


SPREADSHEET_BODY = {
    'properties': {'title': f'{datetime.now().strftime(FORMAT)}',
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
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создает новый документ, возвращая его ID и ссылку на него."""
    service = await wrapper_services.discover('sheets', 'v4')
    SPREADSHEET_BODY.update()
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
    """Разрешает доступ к документу для пользователя по email."""
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
    """Обновляет содержимое документа."""
    service = await wrapper_services.discover('sheets', 'v4')
    current_date = datetime.now().strftime(FORMAT)
    TABLE_VALUES[TABLE_VALUES_DATE_ROW_INDEX][TABLE_VALUES_DATE_COL_INDEX] = (
        current_date
    )
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
        raise ValueError('Невозможно сформировать отчет, так как '
                         'создаваемая таблица слишком велика')
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:{chr(table_cols + UNICODE_START_CHAR_NUM)}'
                  f'{len(TABLE_VALUES)}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
