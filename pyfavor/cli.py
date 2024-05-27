""" """
import rich_click as click

@click.group()
def main():
    """ """
    click.echo(click.style("This is pyfavor", fg='blue'))
    
@click.command()
@click.option("-c", "--confirm", is_flag=True, show_default=True, default=False)
def create(confirm):
    """ """
    print('dupa')
    
main.add_command(create)
