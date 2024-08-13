import io
import flet as ft
from flet import *
import sys
import src.constants as constants
import src.app as app

class CapturingOutput(io.StringIO):
    def __init__(self, text_field):
        super().__init__()
        self.text_field = text_field

    def write(self, s):
        self.text_field.value += s
        self.text_field.update()

def main(page: ft.Page):
    page.title = "Cantaê Tools"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.bgcolor = "#111111"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.width = 700
    page.window.height = 800
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

    # hide all dialogs in overlay
    page.overlay.extend([input_directory, output_directory])

    def create_dropdown(options, label, value=None):
        return Dropdown(
            options=options,
            dense=True,
            border_color="#2e2e2e",
            text_size=12,
            label=label,
            label_style=TextStyle(color="#8e8e8e", size=12),
            bgcolor="#1e1e1e",
            value=value
        )

    #dropdown components
    model_options = [ft.dropdown.Option(option) for option in constants.MODELS]
    dropdown_model = create_dropdown(model_options, "Select a model", "MDX23C-8KFFT-InstVoc_HQ.ckpt")

    format_options = [ft.dropdown.Option(option) for option in constants.OUTPUT_FORMATS]
    dropdown_format = create_dropdown(format_options, "Select a format", "mp3")

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
            on_click=lambda _: function if function() else None,
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
        icons.INPUT,
        input_directory.get_directory_path,
        ink=True,
        child=input_directory_path
    )

    output_card = create_card(
        "Output Directory",
        icons.OUTPUT,
        output_directory.get_directory_path,
        ink=True,
        child=output_directory_path
    )

    model_card = create_card(
        "Model",
        icons.MODEL_TRAINING,
        None,
        100,
        child=dropdown_model
    )

    audio_format_card = create_card(
        "Audio Format",
        icons.AUDIO_FILE,
        None,
        100,
        child=dropdown_format
    )

    # Checkbox components
    separate_audio = create_switch()
    id3_tags = create_switch()
    mid_file = create_switch()
    lyric_file = create_switch()

    separate_card = create_card(
        "Separate",
        icons.CALL_SPLIT,
        None,
        100,
        child=separate_audio
    )

    id3_card = create_card(
        "ID3 Tags",
        icons.LABEL,
        None,
        100,
        child=id3_tags
    )

    midi_card = create_card(
        "MIDI file",
        icons.MUSIC_NOTE,
        None,
        100,
        child=mid_file
    )

    lyric_card = create_card(
        "Lyrics",
        icons.LYRICS,
        None,
        100,
        child=lyric_file
    )

    def close_banner(e):
        page.close(banner)

    # Alert banner
    banner = Banner(
        bgcolor=colors.AMBER_700,
        # leading=Icon(icons.WARNING_AMBER_ROUNDED, color=colors.BLACK, size=40),
        content=Text(
            value="Oops, Input, Output, Model and Format fields are required",
            color=colors.BLACK,
        ),
        actions=[
            TextButton(text="ok", style=ButtonStyle(color="white", bgcolor="black"),  on_click=close_banner)
        ],
    )

    def on_separate(start):

        if start: return

        if not (input_directory_path.value == empty_directory  and input_directory_path.value == empty_directory):
            text_field.value = ""
            start = True
            start_row.controls = [
                ft.ProgressRing(width=16, height=16, stroke_width = 2, color="white"),
                ft.Text("Wait for the completion...", color="white", weight=FontWeight.BOLD, size=14)
            ]
            page.update()
            app.process(
                input_directory_path.value,
                output_directory_path.value,
                dropdown_model.value,
                dropdown_format.value,
                separate_audio.value,
                id3_tags.value,
                mid_file.value,
                lyric_file.value
            )
            start = False
            start_row.controls = [start_text]
            page.update()
        else:
            page.open(banner)

    text_field = TextField(
        multiline=True,
        text_style=TextStyle(color="#8e8e8e", size=14),
        border=None,
        read_only=True,
        border_color="#1e1e1e",
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

    # sys.stdout = PrintRedirector(text_field)
    sys.stdout = CapturingOutput(text_field)
    sys.stderr = CapturingOutput(text_field)

    start_text=ft.Text("Start Process", color="white", weight=FontWeight.BOLD, size=14, disabled=start_process)
    start_row = Row([start_text])

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
                            output_card
                        ]
                    ),
                    Row(
                        spacing=15,
                        controls=[
                            model_card,
                            audio_format_card
                        ]
                    ),
                    Row(
                        spacing=15,
                        controls=[
                            separate_card,
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
                                                Icon(icons.TERMINAL, color="#4e4e4e"),
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