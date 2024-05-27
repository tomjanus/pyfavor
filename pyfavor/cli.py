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
    print("Empty create function")
    
@click.command()
@click.option("-c", "--confirm", is_flag=True, show_default=True, default=False)
def batch_create(confirm):
    """ """
    print("Empty batch-create function")
    
main.add_command(create)
main.add_command(batch_create)
