import click
from click_repl import ExitReplException, repl
from prompt_toolkit import print_formatted_text


def _do_nothing(*args):
    pass


def create(group, prompt_kwargs, *, before_done_callback=_do_nothing):
    """
    Creates a repl for any subcommand, with associated useful commands
    :param group:  the command group to add the function to
    :param prompt_kwargs: keyword args for prompt_toolkit prompt
    :param before_done_callback: function to execute before exiting repl
    :return:
    """
    _add_done(group, before_done_callback)
    _add_help_function(group)
    group.help += " Run with no commands for interactive console."
    _repl_function = _add_repl_function(group, prompt_kwargs)

    def _run_repl(ctx):
        if ctx.invoked_subcommand is None:
            ctx.invoke(_repl_function)

    return _run_repl


def _add_done(group, before_done):
    def _repl_done():
        before_done(click.get_current_context())
        raise ExitReplException

    done_cmd = click.Command('done', callback=_repl_done, help=f'Exit interactive console')
    quit_cmd = click.Command('quit', callback=_repl_done, hidden=True)
    exit_cmd = click.Command('exit', callback=_repl_done, hidden=True)
    group.add_command(done_cmd)
    group.add_command(quit_cmd)
    group.add_command(exit_cmd)


def _add_help_function(group):
    def _generic_help_function():
        ctx = click.get_current_context()
        help_text_lines = group.get_help(ctx).splitlines()
        command_index = help_text_lines.index('Commands:')
        for line in help_text_lines[command_index:]:
            print_formatted_text(line)
    help_cmd = click.Command('help', callback=_generic_help_function, help='Show this message and exit')
    group.add_command(help_cmd)


def _add_repl_function(group, prompt_kwargs):
    def _repl():
        repl(click.get_current_context(), prompt_kwargs=prompt_kwargs)
    repl_cmd = click.Command(f'_{group}_repl', callback=_repl, hidden=True)
    group.add_command(repl_cmd)
    return repl_cmd
