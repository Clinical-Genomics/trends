
from vogue.commands.load.application_tag import application_tags
from vogue.server import create_app
from vogue.commands.base import cli
import pytest

app = create_app()



def test_application_tag(database):
    app.db = database

    ## GIVEN a correct foramted input string
    app_tags = '[{"tag":"MELPCFR030", "category":"wgs"}]'
    
    ## WHEN adding a application tags
    runner = app.test_cli_runner()
    result = runner.invoke(cli, ['load', 'apptag', '-a', app_tags])

    ## THEN assert the new apptag should be added to the colleciton
    assert app.adapter.app_tag('MELPCFR030')['category'] == 'wgs'


def test_application_tag_wrong_input(database):
    app.db = database

    ## GIVEN a badly foramted input string
    app_tags = "[{'tag':'MELPCFR030', 'category':'wgs'}]}"

    ## WHEN adding a application tags
    ## THEN assert error
    runner = app.test_cli_runner()
    with pytest.raises(ValueError):
        result = runner.invoke(cli, ['load', 'apptag', '-a', app_tags])
        #Not working" Need help!