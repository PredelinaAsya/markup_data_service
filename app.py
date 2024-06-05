import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()

    OCR_DATA_FOLDER = os.getenv('OCR_DATA_FOLDER')
    st.title('Сервис для доразметки OCR датасета')

    st.header('Таблица с предразметкой')
    
    premarkup_df_path = os.path.join(OCR_DATA_FOLDER, 'labels.csv')
    premarkup_df = pd.read_csv(premarkup_df_path, encoding='cp1251')
    premarkup_df = premarkup_df[['filename', 'words']]

    st.dataframe(premarkup_df)

    st.header('Доразметка')

    st.text('Выберите начальный и конечный индексы размечаемых картинок:')
    min_id = st.number_input(
        "Выбор начального индекса", value=None,
        min_value=0, max_value=len(premarkup_df) - 1,
    )
    max_id = st.number_input(
        "Выбор конечного индекса", value=None,
        min_value=0, max_value=len(premarkup_df) - 1,
    )

    if min_id is not None and max_id is not None:

        markup_dict = {}

        for crop_id in range(min_id, max_id + 1):
            row = premarkup_df.iloc[crop_id, :]
            img_name = row['filename']
            img_path = os.path.join(OCR_DATA_FOLDER, img_name)

            st.subheader(f'Кроп: {img_name}')
            labeled_text = st.text_input(
                f"Исправьте разметку для {img_name}, если необходимо:",
                value=row['words'],
            )
            st.image(img_path)

            bad_detection = st.checkbox(
                f'В кропе {img_name} есть несколько строчек текста / нет текста вообще => удалить из датасета'
            )
            selected = st.checkbox(f'Кроп {img_name} размечен')

            if selected and not bad_detection:
                markup_dict[img_name] = labeled_text

                saved_df = pd.DataFrame.from_dict(
                    {
                        "filename": list(markup_dict.keys()),
                        "words": list(markup_dict.values()),
                    }
                )

                saved_df.to_csv(f'save_markup_{min_id}_{max_id}.csv')
