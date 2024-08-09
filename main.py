import flet as ft
from flet import *

def main(page: ft.Page):
    page.title = "Audio Separator"
    # page.vertical_alignment = flet.MainAxisAlignment.CENTER

    # Open input directory dialog
    def input_directory_result(e: FilePickerResultEvent):
        input_directory_path.value = e.path if e.path else None
        input_directory_path.update()

    input_directory = FilePicker(on_result=input_directory_result)
    input_directory_path = Text()

    def output_directory_result(e: FilePickerResultEvent):
        output_directory_path.value = e.path if e.path else None
        output_directory_path.update()
        
    output_directory = FilePicker(on_result=output_directory_result)
    output_directory_path = Text()

    # hide all dialogs in overlay
    page.overlay.extend([input_directory, output_directory])

    def on_separate_click():
        if(input_directory_path.value and input_directory_path.value):
            print(input_directory_path.value)

    def enable_separate_button():
        if(input_directory_path.value and input_directory_path.value):
            return False
        return True

    page.add(
        Row(
            [
                ElevatedButton(
                    "Input directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: input_directory.get_directory_path(),
                    disabled=page.web,
                ),
                input_directory_path,
            ]
        ),
        Row(
            [
                ElevatedButton(
                    "Output directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: output_directory.get_directory_path(),
                    disabled=page.web,
                ),
                output_directory_path,
            ]
        ),
         Row(
            [
                Dropdown(
                    label="Model",
                    hint_text="Select a model",
                    default_value="UVR_MDXNET_KARA_2.onnx",
                    options=[
                        ft.dropdown.Option("UVR_MDXNET_KARA_2.onnx"),
                        ft.dropdown.Option("Green"),
                        ft.dropdown.Option("Blue"),
                    ],
                )
            ]
        ),
        Row(
            [
                ElevatedButton(
                    "Separate",
                    icon=icons.CHECK,
                    bgcolor="#ff0000",
                    color="#ffffff",
                    on_click=lambda _: on_separate_click(),
                    # disabled=enable_separate_button(),
                )
            ]
        )
    )


ft.app(target=main)