import os
import platform
import sys
from pathlib import Path

from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication
from parse import parse, Result, Match

from OSCMidiController import OSCMidiController
from Port import Port
from ui import NoteWidget
from ui.OSCMidiWidget import OSCMidiWidget

from configparser import ConfigParser

app: QApplication = None
ui: OSCMidiWidget = None
controller: OSCMidiController = None

permanent_file_path = os.path.join(os.path.expanduser('~'), ".OSCMidi")
template_config_file = "config/default_config.ini"
config_file = "config/config.ini"

if getattr(sys, 'frozen', False):
    # application_path = os.path.dirname(sys.executable)
    application_path = sys._MEIPASS
elif __file__:
    application_path = os.path.dirname(__file__)

absolute_template_config_file = os.path.join(application_path, template_config_file)
absolute_config_file = os.path.join(permanent_file_path, config_file)


settings_section = 'settings'
notes_section = 'notes'

template_config: ConfigParser = ConfigParser()
config: ConfigParser = ConfigParser()

value_mapping_dict = {
    "input": "{name:}",
    "output": "{name:}",
    "particle_enabled": "{enabled:d}",
    "particle_lifetime": "{lifetime:f}",
    "particle_limit_enabled": "{enabled:d}",
    "particle_limit": "{limit:d}",
    "note_text": "{text:}",
    "note_checked": "{checked:d}",
    "search_text": "{text:}"
}

option_mapping_dict = {
    "note_text": "text#{index:d}",
    "note_checked": "checked#{index:d}"
}


def protected_get(parser: ConfigParser, backup_parser: ConfigParser, section: str, option: str, pattern: str,
                  allow_none: bool = False) -> None | Result | Match:

    print("Loading: ", option)
    if not parser.has_section(section):
        parser.add_section(section)

    value: str | None = None
    if parser.has_option(section, option):
        value = parser.get(section, option)

    if value is None or parse(pattern, value) is None:
        if not allow_none or backup_parser.has_option(section, option):
            value = backup_parser.get(section, option)
            print("recovering from backup")

    if value is None:
        return None

    return parse(pattern, value)


def protected_set(parser: ConfigParser, section: str, option: str, pattern: str, *args, **kwargs):
    print("Saving: ", option)
    if not parser.has_section(section):
        parser.add_section(section)

    parser.set(section, option, pattern.format(*args, **kwargs))
    write_config()


def read_config():
    controller.resfreshAvailablePorts()

    result = protected_get(config, template_config, settings_section, 'input', value_mapping_dict['input'], True)
    if result is not None:
        ui.setSelectedInput(result['name'])

    result = protected_get(config, template_config, settings_section, 'output', value_mapping_dict['output'], True)
    if result is not None:
        ui.setSelectedOutput(result['name'])

    ui.setParticlesEnabled(
        protected_get(config, template_config, settings_section, 'particle_enabled', value_mapping_dict['particle_enabled'])[
            'enabled'] > 0)

    ui.setParticleLifeTime(protected_get(config, template_config, settings_section, 'particle_lifetime',
                                         value_mapping_dict['particle_lifetime'])['lifetime'])

    ui.setLimitParticles(protected_get(config, template_config, settings_section, 'particle_limit_enabled',
                                       value_mapping_dict['particle_limit_enabled'])['enabled'] > 0)

    ui.setParticleLimit(
        protected_get(config, template_config, settings_section, 'particle_limit', value_mapping_dict['particle_limit'])[
            'limit'])

    ui.refreshParticleBox()

    # print("Read note configuration")

    i = 0
    while True:
        text_option = option_mapping_dict['note_text'].format(index=i)
        text_result = protected_get(config, template_config, notes_section, text_option, value_mapping_dict['note_text'], True)

        checked_option = option_mapping_dict['note_checked'].format(index=i)
        checked_result = protected_get(config, template_config, notes_section, checked_option, value_mapping_dict['note_checked'], True)

        if text_result is None or checked_result is None:
            break

        text = text_result['text']
        checked = checked_result['checked'] > 0

        print(f"checked: {checked}\ttext: {text}")
        ui.addNoteItem(checked=checked, text=text)
        i = i + 1

    text_result = protected_get(config, template_config, notes_section, 'search_text', value_mapping_dict['search_text'])
    ui.setSearchText("" if text_result is None else text_result['text'])

def save_input_config(input: Port):
    if input is None:
        return

    protected_set(config, settings_section, 'input', value_mapping_dict['input'], name=input.getName())


def save_output_config(output: Port):
    if output is None:
        return

    protected_set(config, settings_section, 'output', value_mapping_dict['output'], name=output.getName())


def save_particle_enabled(enabled: bool):
    protected_set(config, settings_section, 'particle_enabled', value_mapping_dict['particle_enabled'], enabled=int(enabled))


def save_particle_lifetime(lifetime: float):
    protected_set(config, settings_section, 'particle_lifetime', value_mapping_dict['particle_lifetime'], lifetime=lifetime)


def save_particle_limit_enabled(enabled: bool):
    protected_set(config, settings_section, 'particle_limit_enabled', value_mapping_dict['particle_limit_enabled'], enabled=int(enabled))


def save_particle_limit(limit: int):
    protected_set(config, settings_section, 'particle_limit', value_mapping_dict['particle_limit'], limit=limit)


def write_config():
    Path(absolute_config_file).parent.mkdir(parents=True, exist_ok=True)

    with open(absolute_config_file, 'w') as f:
        config.write(f)


def save_notes_config(notes:[NoteWidget]):
    config.remove_section(notes_section)
    config.add_section(notes_section)

    for i in range(0, len(notes)):
        text_option = option_mapping_dict['note_text'].format(index=i)
        checked_option = option_mapping_dict['note_checked'].format(index=i)

        protected_set(config, notes_section, text_option, value_mapping_dict['note_text'], text=notes[i].getText())
        protected_set(config, notes_section, checked_option, value_mapping_dict['note_checked'], checked=int(notes[i].isChecked()))


def save_search_text(text: str):
    protected_set(config, notes_section, 'search_text', value_mapping_dict['search_text'], text=text)

def connect_config():
    ui.on_selected_input_change += save_input_config
    ui.on_selected_output_change += save_output_config

    ui.on_particle_enabled_change += save_particle_enabled
    ui.on_particle_lifetime_change += save_particle_lifetime

    ui.on_particle_limit_enabled_change += save_particle_limit_enabled
    ui.on_particle_limit_change += save_particle_limit

    ui.on_notes_change += save_notes_config
    ui.on_search_text_change += save_search_text


def setAppStyle():
    app_platform = platform.system()
    window_desired_style = 'Fusion'

    if app_platform == 'Windows' and window_desired_style in QtWidgets.QStyleFactory.keys():
        app.setStyle(window_desired_style)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    setAppStyle()
    ui = OSCMidiWidget()
    controller = OSCMidiController(ui, '127.0.0.1')

    # 192.168.0.167

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        #application_path = os.path.dirname(sys.executable)
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)

    template_config.read(absolute_template_config_file)
    config.read(absolute_config_file)

    read_config()

    connect_config()

    sys.exit(app.exec())
