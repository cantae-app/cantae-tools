import flet as ft
from flet import *
import constants
# import app

def main(page: ft.Page):
    page.title = "Audio Separator"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.bgcolor = "#111111"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    # page.vertical_alignment = flet.MainAxisAlignment.CENTER

    # input directory components
    def input_directory_result(e: FilePickerResultEvent):
        input_directory_path.value = e.path if e.path else None
        input_directory_path.update()

    input_directory = FilePicker(on_result=input_directory_result)
    input_directory_path = Text(
        "No directory selected",
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
        color="#8e8e8e",
        size=12
    )

    def output_directory_result(e: FilePickerResultEvent):
        output_directory_path.value = e.path if e.path else None
        output_directory_path.update()

    output_directory = FilePicker(on_result=output_directory_result)
    output_directory_path = Text(
        "No directory selected",
        overflow=ft.TextOverflow.ELLIPSIS,
        max_lines=1,
        color="#8e8e8e",
        size=12
    )

    # hide all dialogs in overlay
    page.overlay.extend([input_directory, output_directory])

    #dropdown components
    model_options = [ft.dropdown.Option(option) for option in constants.MODELS]
    dropdown_model = Dropdown(
        options=model_options,
        dense=True,
        border_color="#2e2e2e",
        text_size=12,
        label="Select a model",
        label_style=TextStyle(color="#8e8e8e", size=12),
        bgcolor="#1e1e1e"
    )

    format_options = [ft.dropdown.Option(option) for option in constants.OUTPUT_FORMATS]
    dropdown_format = Dropdown(
        options=format_options,
        dense=True,
        border_color="#2e2e2e",
        text_size=12,
        label="Select a format",
        label_style=TextStyle(color="#8e8e8e", size=12),
        bgcolor="#1e1e1e"
    )

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

    # Card components
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
    mid_file = create_switch(False)
    lyric_file = create_switch(False)

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
    
    

    def on_separate_click():
        empty = "No directory selected"
        if not (input_directory_path.value == empty  and input_directory_path.value == empty):
            print(input_directory_path.value)
            # app.process(
            #     input_directory_path.value,
            #     output_directory_path.value,
            #     dropdown_model.value,
            #     dropdown_format.value,
            #     separate_audio.value,
            #     id3_tags.value,
            #     mid_file.value,
            #     lyric_file.value
            # )
        else:
            page.open(banner)

    def enable_separate_button():
        if(input_directory_path.value and input_directory_path.value):
            return False
        return True

    page.add(
        Column(
            spacing=15,
            controls=[
                Container(
                    content=Image(
                        src="assets/images/logo.png",
                        height=40,
                    ),
                ),
                Row(
                    # alignment=MainAxisAlignment.SPACE_BETWEEN,
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
                            expand=True,
                            border_radius=10,
                            bgcolor="#e11d48",
                            padding=12,
                            on_click=lambda _: on_separate_click(),
                            ink=True,
                            content=Text(
                                "Separate",
                                color="white",
                                size=14,
                                weight=FontWeight.BOLD
                            ),
                        ),
                    ]
                )
            ]
        )
    )


ft.app(target=main, view=ft.AppView.WEB_BROWSER)