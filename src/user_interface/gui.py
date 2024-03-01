import datetime
import tkinter as tk
from tkinter import filedialog, ttk

import tkcalendar

import config.config as cfg
import parse.parse
import store.csv

_content_filters = []


def launch(
    result_text_widget,
    parser_opt,
    output_opt,
    allowed_content,
    start_date,
    end_date,
    input_file,
):
    if output_opt == "stdout":
        text_widget_set(
            result_text_widget, "Output option: stdout is not supported in gui mode"
        )
        return

    if not input_file:
        text_widget_set(result_text_widget, "You need to select a chat log")
        return
    if not parser_opt or not parser_opt in cfg.allowed_parser_opts:
        text_widget_set(result_text_widget, "Invalid parser option")
        return
    if not output_opt or not output_opt in cfg.allowed_ouput_opts:
        text_widget_set(result_text_widget, "Invalid output option")
        return

    start_date_parsed = None
    end_date_parsed = None
    if start_date:
        start_date_parsed = datetime.datetime.strptime(start_date, "%d/%m/%y").date()
    if end_date:
        end_date_parsed = datetime.datetime.strptime(end_date, "%d/%m/%y").date()

    filter = cfg.Filter(allowed_content, start_date_parsed, end_date_parsed, None, None)

    match output_opt:
        case "csv":
            store.csv.write_all(
                parse.parse.yield_message(input_file, parser_opt, filter)
            )
    text_widget_set(result_text_widget, "Done")


def add_content_filter_entry(parent, filter_canvas, filter_frame):
    remove_btn = ttk.Button(parent, text="-", width=2)
    entry = ttk.Entry(parent)

    _content_filters.append((entry, remove_btn))

    index = _content_filters.index((entry, remove_btn))

    remove_btn.configure(
        command=lambda: remove_content_filter_entry(
            (entry, remove_btn), filter_canvas, filter_frame
        )
    )

    remove_btn.grid(column=0, row=index, sticky="w", padx=5, pady=5)
    entry.grid(column=1, row=index, sticky="we", padx=5, pady=5)
    update_scroll_region(filter_canvas, filter_frame)


def remove_content_filter_entry(entry_btn_tuple, filter_canvas, filter_frame):
    index = _content_filters.index(entry_btn_tuple)
    entry, remove_btn = _content_filters.pop(index)
    entry.grid_forget()
    remove_btn.grid_forget()
    update_scroll_region(filter_canvas, filter_frame)


def grab_date(date_label, date_window, calendar):
    entry_set_text(date_label, calendar.get_date())
    date_window.destroy()


def pick_date_dialog(dialog_title, date_label):
    date_window = tk.Toplevel()
    # date_window.grab_set()
    date_window.wm_title(dialog_title)
    date_window.geometry("250x220")
    calendar_frame = ttk.Frame(date_window)
    calendar = tkcalendar.Calendar(
        calendar_frame, selectmode="day", date_pattern="dd/mm/yy"
    )

    calendar_frame.grid(column=0, row=0)
    calendar.grid(column=0, row=0, sticky="nswe")

    submit_btn = ttk.Button(
        calendar_frame,
        text="Submit",
        command=lambda: grab_date(date_label, date_window, calendar),
    )
    submit_btn.grid(column=0, row=1)
    date_window.columnconfigure(0, weight=1)
    date_window.rowconfigure(0, weight=1)
    calendar_frame.columnconfigure(0, weight=1)
    calendar_frame.rowconfigure(0, weight=1)


def entry_set_text(entry, text):
    entry.delete(0, tk.END)
    entry.insert(0, text)


def text_widget_set(text_widget, content):
    text_widget.configure(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, content)
    text_widget.configure(state=tk.DISABLED)


def on_mousewheel(event, canvas):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def update_scroll_region(canvas, frame):
    canvas.update_idletasks()
    canvas.config(scrollregion=frame.bbox("all"))


def run(config, chat_log_fname):
    root = tk.Tk()
    root.wm_title("OverInsight 1.0.0")
    root.geometry("1000x500")
    root.minsize(1000, 500)

    content = ttk.Frame(root, padding=(3, 3, 12, 12))

    # Config frame
    config_frame = ttk.LabelFrame(content, text="Configuration")

    parser_combo_var = tk.StringVar()
    parser_combo = ttk.Combobox(
        config_frame,
        textvariable=parser_combo_var,
        state="readonly",
        values=cfg.allowed_parser_opts,
    )
    parser_label = ttk.Label(config_frame, text="Select a parser")
    if config.parser:
        parser_combo.set(config.parser)

    output_combo_var = tk.StringVar()
    output_combo = ttk.Combobox(
        config_frame,
        textvariable=output_combo_var,
        state="readonly",
        values=cfg.allowed_ouput_opts,
    )
    output_label = ttk.Label(config_frame, text="Select an output format")
    if config.output:
        output_combo.set(config.output)

    filter_frame = ttk.LabelFrame(config_frame, text="Filter")

    allowed_content_frame = ttk.LabelFrame(filter_frame, text="Allowed content")

    start_date_label = ttk.Label(filter_frame, text="Start date (inclusive)")
    end_date_label = ttk.Label(filter_frame, text="End date (inclusive)")
    start_date_value = ttk.Entry(filter_frame)
    start_date_value.bind(
        "<Button-1>", lambda _: pick_date_dialog("Pick a date", start_date_value)
    )
    end_date_value = ttk.Entry(filter_frame)
    end_date_value.bind(
        "<Button-1>", lambda _: pick_date_dialog("Pick a date", end_date_value)
    )

    content_entry_container = ttk.Frame(allowed_content_frame)
    content_entry_canvas = tk.Canvas(
        content_entry_container,
        # highlightthickness=0,
    )
    content_entry_frame = ttk.Frame(content_entry_canvas)
    scrollbar = tk.Scrollbar(content_entry_container, orient=tk.VERTICAL)
    content_entry_canvas.create_window((0, 0), window=content_entry_frame)
    content_entry_canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.config(command=content_entry_canvas.yview)

    content_entry_canvas.bind_all(
        "<MouseWheel>", lambda event: on_mousewheel(event, content_entry_canvas)
    )

    add_content_entry_btn = ttk.Button(
        allowed_content_frame,
        text="+",
        command=lambda: add_content_filter_entry(
            content_entry_frame, content_entry_canvas, content_entry_frame
        ),
    )

    # File frame
    command_frame = ttk.LabelFrame(content, text="Command")
    input_file_label = ttk.Label(command_frame, text="Chat:")
    input_file_value = ttk.Entry(command_frame)
    input_file_dialog = ttk.Button(
        command_frame,
        text="Select a chat log",
        command=lambda: entry_set_text(input_file_value, filedialog.askopenfilename()),
    )

    output_frame = ttk.LabelFrame(command_frame, text="Output")
    result_text = tk.Text(output_frame, state=tk.DISABLED, height=10)
    run_btn = ttk.Button(
        output_frame,
        text="Run",
        command=lambda: launch(
            result_text,
            parser_combo_var.get(),
            output_combo_var.get(),
            [entry.get() for entry, _ in _content_filters],
            start_date_value.get(),
            end_date_value.get(),
            input_file_value.get(),
        ),
    )

    # Root grid
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    content.grid(column=0, row=0, sticky="nswe")

    # Content grid
    config_frame.grid(column=0, row=0, sticky="nswe")
    command_frame.grid(column=1, row=0, sticky="nsew")
    content.columnconfigure(0, weight=1)
    content.columnconfigure(1, weight=3)
    content.rowconfigure(0, weight=1)

    # File frame grid
    input_file_label.grid(column=0, row=0, sticky="nswe", padx=5, pady=5)
    input_file_value.grid(column=1, row=0, sticky="nswe", padx=5, pady=5)
    input_file_dialog.grid(column=2, row=0, padx=5, pady=5)
    output_frame.grid(column=0, row=10, columnspan=3, sticky="swe")
    command_frame.columnconfigure(0, weight=0)
    command_frame.columnconfigure(1, weight=1)
    command_frame.columnconfigure(2, weight=0)
    command_frame.rowconfigure(10, weight=1)

    # output_frame grid
    result_text.grid(column=0, row=0, sticky="nswe", padx=5, pady=5)
    run_btn.grid(column=0, row=1, pady=10)
    output_frame.columnconfigure(0, weight=1)

    # ConfigFrame grid
    parser_label.grid(column=0, row=0, sticky="nwe", padx=5, pady=1)
    parser_combo.grid(column=0, row=1, sticky="nwe", padx=5, pady=5)
    output_label.grid(column=0, row=2, sticky="nwe", padx=5, pady=1)
    output_combo.grid(column=0, row=3, sticky="nwe", padx=5, pady=5)
    filter_frame.grid(column=0, row=4, sticky="nswe", padx=5, pady=5)
    config_frame.columnconfigure(0, weight=1)
    config_frame.rowconfigure(4, weight=1)

    # FilterFrame grid
    allowed_content_frame.grid(column=0, row=0, sticky="nswe", padx=5, pady=5)
    start_date_label.grid(column=0, row=2, sticky="nswe", padx=5, pady=1)
    start_date_value.grid(column=0, row=3, sticky="nswe", padx=5, pady=5)
    end_date_label.grid(column=0, row=4, sticky="nswe", padx=5, pady=1)
    end_date_value.grid(column=0, row=5, sticky="nswe", padx=5, pady=5)
    filter_frame.columnconfigure(0, weight=1)
    filter_frame.rowconfigure(0, weight=1)

    # AllowedContent grid
    add_content_entry_btn.grid(column=0, row=0, padx=5, pady=5)
    content_entry_container.grid(column=0, row=1, sticky="nswe", padx=5, pady=5)
    allowed_content_frame.columnconfigure(0, weight=1)
    allowed_content_frame.rowconfigure(1, weight=1)

    # Content entry container grid
    content_entry_canvas.grid(column=0, row=0, sticky="nswe")
    scrollbar.grid(column=1, row=0, sticky="ns")
    content_entry_container.rowconfigure(0, weight=1)
    content_entry_container.columnconfigure(0, weight=1)

    # Content canvas grid
    content_entry_frame.grid(column=0, row=0, sticky="nswe", padx=5, pady=5)
    content_entry_canvas.columnconfigure(0, weight=1)
    content_entry_canvas.rowconfigure(0, weight=1)

    # Content frame grid
    content_entry_frame.columnconfigure(1, weight=1)

    root.mainloop()
