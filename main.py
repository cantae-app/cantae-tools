
import sys
sys.path.append('src') 

import flet as ft
from flet import *
from capturing_output import CapturingOutput
import constants as contants
import inference as inference
import json

def main(page: ft.Page):
    page.title = "Cantaê Tools"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.bgcolor = "#111111"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.width = 800
    page.window.height = 800
    page.window.min_width = 700
    page.window.min_height = 800
    page.window.reziable = False
    empty_directory = "No directory selected"
    start_process = False

    # input directory components
    def input_directory_result(e: FilePickerResultEvent):
        input_directory_path.value = e.path if e.path else empty_directory
        input_directory_path.update()

    input_directory = FilePicker(on_result=input_directory_result)
    input_directory_path = Text(
        empty_directory,
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
        color="#8e8e8e",
        size=12
    )

    def output_directory_result(e: FilePickerResultEvent):
        output_directory_path.value = e.path if e.path else empty_directory
        output_directory_path.update()

    output_directory = FilePicker(on_result=output_directory_result)
    output_directory_path = Text(
        empty_directory,
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
        color="#8e8e8e",
        size=12
    )

    def output_model_result(e: FilePickerResultEvent):
        output_model_path.value = e.path if e.path else empty_directory
        output_model_path.update()

    output_model = FilePicker(on_result=output_model_result)
    output_model_path = Text(
        empty_directory,
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
        color="#8e8e8e",
        size=12
    )

    # hide all dialogs in overlay
    page.overlay.extend([input_directory, output_directory, output_model])

    def create_dropdown(options, label, value=None, on_change=None):
        return Dropdown(
            options=options,
            dense=True,
            border_color="#2e2e2e",
            text_size=12,
            label=label,
            label_style=TextStyle(color="#8e8e8e", size=12),
            bgcolor="#1e1e1e",
            value=value,
            on_change=on_change,
        )

    #dropdown components
    model_options = [ft.dropdown.Option(option) for option in contants.MODELS['mdxnet']]
    dropdown_model = create_dropdown(model_options, "Select a model", "UVR_MDXNET_KARA.onnx")

    format_options = [ft.dropdown.Option(option) for option in contants.OUTPUT_FORMATS]
    dropdown_format = create_dropdown(format_options, "Select a format", "mp3")

    def on_selecte_model(e: ft.ControlEvent):
        model_options = [ft.dropdown.Option(option) for option in contants.MODELS[e.control.value]]
        dropdown_model.options = model_options
        dropdown_model.update()
        
    process_options = [ft.dropdown.Option(option) for option in contants.MODELS]
    dropdown_process = create_dropdown(process_options, "Select process", "mdxnet", on_selecte_model)

    

    def create_switch(value=True):
        return Switch(
            value=value,
            scale=0.7,
            active_color="white",
            active_track_color="#e11d48",
            inactive_track_color="#2e2e2e",
            inactive_thumb_color="white",
            track_outline_color="#2e2e2e",
        )

    def create_card(title, icon, function, height=70, ink=False, child=None):
        return Container(
            expand=True,
            height=height,
            border_radius=10,
            bgcolor="#1e1e1e",
            on_click=lambda _: function() if function is not None else None,
            padding=12,
            ink=ink,
            content=Column(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
                controls=[
                    Row(
                        [
                            Icon(icon, color="#4e4e4e"),
                            Text(title, color="white", weight=FontWeight.BOLD, size=14),
                        ]
                    ),
                    child
                ]
            )
        )

    input_card = create_card(
        "Input Directory",
        Icons.INPUT,
        input_directory.get_directory_path,
        ink=True,
        child=input_directory_path
    )

    output_card = create_card(
        "Output Directory",
        Icons.OUTPUT,
        output_directory.get_directory_path,
        ink=True,
        child=output_directory_path
    )

    output_model = create_card(
        "Model Directory",
        Icons.OUTPUT,
        output_model.get_directory_path,
        ink=True,
        child=output_model_path
    )

    process_card = create_card(
        "Process",
        Icons.MODEL_TRAINING,
        None,
        100,
        child=dropdown_process
    )

    model_card = create_card(
        "Model",
        Icons.MODEL_TRAINING,
        None,
        100,
        child=dropdown_model
    )

    audio_format_card = create_card(
        "Audio Format",
        Icons.AUDIO_FILE,
        None,
        100,
        child=dropdown_format
    )

    # Checkbox components
    # separate_audio = create_switch()
    id3_tags = create_switch()
    mid_file = create_switch()
    lyric_file = create_switch()

    # separate_card = create_card(
    #     "Separate",
    #     Icons.CALL_SPLIT,
    #     None,
    #     100,
    #     child=separate_audio
    # )

    id3_card = create_card(
        "ID3 Tags",
        Icons.LABEL,
        None,
        100,
        child=id3_tags
    )

    midi_card = create_card(
        "MIDI file",
        Icons.MUSIC_NOTE,
        None,
        100,
        child=mid_file
    )

    lyric_card = create_card(
        "Lyrics",
        Icons.LYRICS,
        None,
        100,
        child=lyric_file
    )

    def close_banner(e):
        page.close(banner)

    # Alert banner
    banner = Banner(
        bgcolor=Colors.AMBER_700,
        # leading=Icon(Icons.WARNING_AMBER_ROUNDED, color=Colors.BLACK, size=40),
        content=Text(
            value="Oops, Input, Output, Model and Format fields are required",
            color=Colors.BLACK,
        ),
        actions=[
            TextButton(text="ok", style=ButtonStyle(color="white", bgcolor="black"),  on_click=close_banner)
        ],
    )

    def on_separate(start):

        if start: return

        if not (input_directory_path.value == empty_directory  and input_directory_path.value == empty_directory):

            # save settings in client storage
            storageData = {
                "input_directory_path": input_directory_path.value,
                "output_directory_path": output_directory_path.value,
                "output_model_path": output_model_path.value,
                "dropdown_model": dropdown_model.value,
                "dropdown_format": dropdown_format.value,
                "id3_tags": id3_tags.value,
                "mid_file": mid_file.value,
                "lyric_file": lyric_file.value,
            }

            page.client_storage.set("settings", json.dumps(storageData))

            text_field.value = ""
            start = True
            start_row.controls = [
                ft.ProgressRing(width=16, height=16, stroke_width = 2, color="white"),
                ft.Text("Processing...", color="white", weight=FontWeight.BOLD, size=14)
            ]
            page.update()
            inference.process(
                input_directory_path.value,
                output_directory_path.value,
                output_model_path.value,
                dropdown_model.value,
                dropdown_format.value,
                id3_tags.value,
                mid_file.value,
                lyric_file.value,
            )
            start = False
            start_row.controls = [start_text]
            page.update()
        else:
            page.open(banner)

    # text_field = TextField(
    #     multiline=True,
    #     text_style=TextStyle(color="#8e8e8e", size=14),
    #     border=None,
    #     read_only=True,
    #     border_color="#1e1e1e",
    # )

    text_field = Text(
        "",
        selectable=True,
        font_family="Courier New",
        size=12,
    )

    scroll_log = Column(
        spacing=10,
        height=200,
        scroll=ft.ScrollMode.ALWAYS,
        auto_scroll=True,
        controls=[
            text_field,
        ]
    )

    sys.stdout = CapturingOutput(text_field)
    sys.stderr = CapturingOutput(text_field)

    start_text=ft.Text("Start Process", color="white", weight=FontWeight.BOLD, size=14, disabled=start_process)
    start_row = Row([start_text])

    # load settings from client storage
    settings = page.client_storage.get("settings")
    if settings:
        settings = json.loads(settings)
        input_directory_path.value = settings["input_directory_path"]
        output_directory_path.value = settings["output_directory_path"]
        output_model_path.value = settings["output_model_path"]
        dropdown_model.value = settings["dropdown_model"]
        dropdown_format.value = settings["dropdown_format"]
        id3_tags.value = settings["id3_tags"]
        mid_file.value = settings["mid_file"]
        lyric_file.value = settings["lyric_file"]

    page.add(
        Container(
            content=Column(
            expand=True,
            spacing=15,
            controls=[
                    Container(
                        content=Image(
                            src="assets/logo.png",
                            height=40,
                        ),
                    ),
                    Row(
                        spacing=15,
                        controls=[
                            input_card,
                            output_card,
                            output_model
                        ]
                    ),
                    Row(
                        spacing=15,
                        controls=[
                            process_card,
                            model_card,
                            audio_format_card
                        ]
                    ),
                    Row(
                        spacing=15,
                        controls=[
                            # separate_card,
                            id3_card,
                            midi_card,
                            lyric_card
                        ]
                    ),
                    Row(
                        spacing=15,
                        controls=[
                            Container(
                                border_radius=10,
                                bgcolor="#e11d48",
                                padding=12,
                                on_click=lambda _: on_separate(start_process),
                                ink=True,
                                content=start_row
                            ),
                        ]
                    ),
                    # Container(
                    #     content=Column(
                    #         expand=True,
                    #         alignment=MainAxisAlignment.SPACE_BETWEEN,
                    #         controls=[
                    #             progress
                    #         ]
                    #     )
                    # ),
                    Row(
                        spacing=15,
                        controls=[
                            Container(
                                bgcolor="#1e1e1e",
                                border_radius=10,
                                padding=12,
                                expand=True,
                                content=Column(
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    expand=True,
                                    controls=[
                                        Row(
                                            [
                                                Icon(Icons.TERMINAL, color="#4e4e4e"),
                                                Text("Log", color="white", weight=FontWeight.BOLD, size=14),
                                            ]
                                        ),
                                        scroll_log
                                    ]
                                )
                            ),
                        ]
                    ),
                ]
            ),
        ),
    )


ft.app(target=main, view=ft.AppView.WEB_BROWSER)